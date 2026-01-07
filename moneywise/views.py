"""
Vues pour l'application MoneyWise - Assistant Financier Intelligent
"""

import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import numpy as np
from datetime import datetime, timedelta

# ==================== VUES PRINCIPALES ====================

def home(request):
    """Page d'accueil avec dashboard"""
    assistant = settings.FINANCIAL_ASSISTANT
    
    # Données pour le template
    context = {
        'transactions': assistant.transactions[-10:][::-1],  # 10 dernières
        'analysis': assistant.get_spending_analysis(),
        'predictions': assistant.predict_next_week(),
        'recommendations': assistant.get_savings_recommendations()[:3],
        'total_balance': sum(t['amount'] for t in assistant.transactions),
        'categories': list(assistant.categories.keys()),
        'budgets': assistant.budgets
    }
    
    return render(request, 'index.html', context)

@csrf_exempt
def api_add_transaction(request):
    """API pour ajouter une transaction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = float(data.get('amount', 0))
            category = data.get('category', 'autres')
            description = data.get('description', '')
            
            assistant = settings.FINANCIAL_ASSISTANT
            transaction = assistant.add_transaction(amount, category, description)
            
            return JsonResponse({
                'success': True,
                'transaction': transaction,
                'message': 'Transaction ajoutée avec succès'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def api_predict(request):
    """API pour obtenir des prédictions"""
    assistant = settings.FINANCIAL_ASSISTANT
    predictions = assistant.predict_next_week()
    
    if predictions:
        return JsonResponse({
            'success': True,
            'predictions': predictions
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Pas assez de données pour la prédiction'
        })

def api_analysis(request):
    """API pour l'analyse des dépenses"""
    assistant = settings.FINANCIAL_ASSISTANT
    analysis = assistant.get_spending_analysis()
    
    return JsonResponse({
        'success': True,
        'analysis': analysis
    })

@csrf_exempt
def api_train_model(request):
    """API pour forcer l'entraînement du modèle"""
    if request.method == 'POST':
        assistant = settings.FINANCIAL_ASSISTANT
        assistant.train_model()
        
        return JsonResponse({
            'success': True,
            'message': 'Modèle ré-entraîné avec succès',
            'loss_history': assistant.network.loss_history[-10:] if assistant.network.loss_history else []
        })
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def api_recommendations(request):
    """API pour obtenir des recommandations"""
    assistant = settings.FINANCIAL_ASSISTANT
    recommendations = assistant.get_savings_recommendations()
    
    return JsonResponse({
        'success': True,
        'recommendations': recommendations
    })

@csrf_exempt
def api_set_budget(request):
    """API pour définir un budget"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = data.get('category')
            budget = float(data.get('budget', 0))
            
            assistant = settings.FINANCIAL_ASSISTANT
            if category in assistant.budgets:
                assistant.budgets[category] = budget
                
                return JsonResponse({
                    'success': True,
                    'message': f'Budget {category} mis à jour à {budget}€'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Catégorie non valide'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def api_transactions(request):
    """API pour obtenir toutes les transactions"""
    assistant = settings.FINANCIAL_ASSISTANT
    
    return JsonResponse({
        'success': True,
        'transactions': assistant.transactions,
        'count': len(assistant.transactions)
    })

def api_statistics(request):
    """API pour les statistiques détaillées"""
    assistant = settings.FINANCIAL_ASSISTANT
    transactions = assistant.transactions
    
    if not transactions:
        return JsonResponse({
            'success': True,
            'statistics': {}
        })
    
    # Calculs statistiques
    amounts = [t['amount'] for t in transactions]
    positive_amounts = [a for a in amounts if a > 0]
    negative_amounts = [a for a in amounts if a < 0]
    
    stats = {
        'total_transactions': len(transactions),
        'average_income': np.mean(positive_amounts) if positive_amounts else 0,
        'average_expense': np.mean(negative_amounts) if negative_amounts else 0,
        'total_income': sum(positive_amounts),
        'total_expenses': abs(sum(negative_amounts)),
        'savings_rate': (sum(positive_amounts) - abs(sum(negative_amounts))) / sum(positive_amounts) * 100 if sum(positive_amounts) > 0 else 0,
        'largest_income': max(positive_amounts) if positive_amounts else 0,
        'largest_expense': min(negative_amounts) if negative_amounts else 0,
        'transaction_frequency': len(transactions) / max(1, (datetime.now() - datetime.strptime(transactions[0]['date'], "%Y-%m-%d %H:%M:%S")).days)
    }
    
    return JsonResponse({
        'success': True,
        'statistics': stats
    })

def api_weekly_report(request):
    """API pour un rapport hebdomadaire"""
    assistant = settings.FINANCIAL_ASSISTANT
    transactions = assistant.transactions
    
    if len(transactions) < 7:
        return JsonResponse({
            'success': False,
            'message': 'Pas assez de données'
        })
    
    # Transactions de la semaine dernière
    week_ago = datetime.now() - timedelta(days=7)
    weekly_transactions = [
        t for t in transactions 
        if datetime.strptime(t['date'], "%Y-%m-%d %H:%M:%S") >= week_ago
    ]
    
    # Analyse hebdomadaire
    weekly_analysis = {
        'total': sum(t['amount'] for t in weekly_transactions),
        'income': sum(t['amount'] for t in weekly_transactions if t['amount'] > 0),
        'expenses': abs(sum(t['amount'] for t in weekly_transactions if t['amount'] < 0)),
        'count': len(weekly_transactions),
        'by_day': {},
        'top_categories': {}
    }
    
    # Par jour
    for i in range(7):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_transactions = [
            t for t in weekly_transactions 
            if t['date'].startswith(day)
        ]
        weekly_analysis['by_day'][day] = {
            'count': len(day_transactions),
            'total': sum(t['amount'] for t in day_transactions)
        }
    
    # Par catégorie
    for category in assistant.categories:
        cat_amount = sum(t['amount'] for t in weekly_transactions 
                       if t.get('category') == category and t['amount'] < 0)
        if cat_amount < 0:
            weekly_analysis['top_categories'][category] = abs(cat_amount)
    
    return JsonResponse({
        'success': True,
        'weekly_report': weekly_analysis
    })

def api_health(request):
    """API de santé du système"""
    assistant = settings.FINANCIAL_ASSISTANT
    
    health_status = {
        'system': 'operational',
        'transactions_count': len(assistant.transactions),
        'model_trained': len(assistant.network.loss_history) > 0,
        'last_training_loss': assistant.network.loss_history[-1] if assistant.network.loss_history else None,
        'cache_available': True,
        'predictions_available': len(assistant.transactions) >= 7
    }
    
    return JsonResponse({
        'success': True,
        'health': health_status
    })

# ==================== VUES DE DÉMONSTRATION ====================

def demo_add_sample_data(request):
    """Vue pour ajouter des données de démonstration"""
    assistant = settings.FINANCIAL_ASSISTANT
    
    # Données de démonstration
    sample_transactions = [
        {'amount': 2500, 'category': 'salaire', 'description': 'Salaire mensuel'},
        {'amount': -800, 'category': 'loyer', 'description': 'Loyer appartement'},
        {'amount': -300, 'category': 'nourriture', 'description': 'Courses semaine'},
        {'amount': -150, 'category': 'transport', 'description': 'Essence'},
        {'amount': -200, 'category': 'loisirs', 'description': 'Restaurant'},
        {'amount': -100, 'category': 'sante', 'description': 'Médecin'},
        {'amount': -50, 'category': 'education', 'description': 'Livres'},
        {'amount': 500, 'category': 'autres', 'description': 'Prime'},
        {'amount': -120, 'category': 'nourriture', 'description': 'Supermarché'},
        {'amount': -80, 'category': 'transport', 'description': 'Taxi'},
    ]
    
    for transaction in sample_transactions:
        assistant.add_transaction(
            transaction['amount'],
            transaction['category'],
            transaction['description']
        )
    
    # Entraîner le modèle
    assistant.train_model()
    
    return JsonResponse({
        'success': True,
        'message': f'{len(sample_transactions)} transactions de démonstration ajoutées',
        'total_transactions': len(assistant.transactions)
    })

def reset_data(request):
    """Vue pour réinitialiser les données (démo uniquement)"""
    assistant = settings.FINANCIAL_ASSISTANT
    assistant.transactions = []
    assistant.save_data()
    
    return JsonResponse({
        'success': True,
        'message': 'Données réinitialisées'
    })