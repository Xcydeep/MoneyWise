"""
Django settings for moneywise project.
"""

import os
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
import json
from django.core.cache import cache

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moneywise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'moneywise.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDERS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== RÉSEAU DE NEURONES ET LOGIQUE MÉTIER ====================

class NeuralNetwork:
    """Réseau de neurones simple pour prédiction financière"""
    
    def __init__(self, input_size=7, hidden_size=10, output_size=1, learning_rate=0.01):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Initialisation des poids avec He initialization
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2. / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2. / hidden_size)
        self.b2 = np.zeros((1, output_size))
        
        self.loss_history = []
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def relu_derivative(self, x):
        return (x > 0).astype(float)
    
    def forward(self, X):
        # Propagation avant
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        return self.z2
    
    def backward(self, X, y, output):
        # Rétropropagation
        m = X.shape[0]
        
        # Calcul des gradients
        dZ2 = output - y.reshape(-1, 1)
        dW2 = (1/m) * np.dot(self.a1.T, dZ2)
        db2 = (1/m) * np.sum(dZ2, axis=0, keepdims=True)
        
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(self.z1)
        dW1 = (1/m) * np.dot(X.T, dZ1)
        db1 = (1/m) * np.sum(dZ1, axis=0, keepdims=True)
        
        # Mise à jour des poids
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        
        # Calcul de la perte
        loss = np.mean((output - y.reshape(-1, 1)) ** 2)
        self.loss_history.append(loss)
        return loss
    
    def train(self, X, y, epochs=1000):
        for epoch in range(epochs):
            output = self.forward(X)
            loss = self.backward(X, y, output)
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
    
    def predict(self, X):
        return self.forward(X)

class FinancialDataProcessor:
    """Processeur de données financières"""
    
    @staticmethod
    def prepare_training_data(transactions):
        """Prépare les données pour l'entraînement"""
        if len(transactions) < 10:
            return None, None
        
        features = []
        targets = []
        
        for i in range(len(transactions) - 7):
            # 7 jours d'historique pour prédire le jour suivant
            week_data = transactions[i:i+7]
            
            # Features: montants des 7 derniers jours, jour de la semaine, mois
            amounts = [t['amount'] for t in week_data]
            days_of_week = [t['day_of_week'] for t in week_data]
            
            # Normalisation
            max_amount = max(abs(a) for a in amounts) if max(abs(a) for a in amounts) > 0 else 1
            normalized_amounts = [a / max_amount for a in amounts]
            
            # Construction du vecteur de features
            feature_vector = normalized_amounts + [
                days_of_week[-1] / 7,
                week_data[-1]['month'] / 12,
                1 if week_data[-1]['is_weekend'] else 0,
                week_data[-1]['category_encoded'] / 10
            ]
            
            features.append(feature_vector)
            targets.append(transactions[i+7]['amount'])
        
        return np.array(features), np.array(targets)

class FinancialAssistant:
    """Assistant financier principal"""
    
    def __init__(self):
        self.network = NeuralNetwork(input_size=11, hidden_size=15)
        self.transactions = []
        self.categories = {
            'loyer': 0, 'nourriture': 1, 'transport': 2, 'loisirs': 3,
            'sante': 4, 'education': 5, 'shopping': 6, 'autres': 7
        }
        self.budgets = {category: 500 for category in self.categories}
        self.load_data()
    
    def load_data(self):
        """Charge les données depuis le cache Django"""
        data = cache.get('financial_data')
        if data:
            self.transactions = json.loads(data)
    
    def save_data(self):
        """Sauvegarde les données dans le cache Django"""
        cache.set('financial_data', json.dumps(self.transactions), timeout=None)
    
    def add_transaction(self, amount, category, description=""):
        """Ajoute une nouvelle transaction"""
        now = datetime.now()
        transaction = {
            'id': len(self.transactions),
            'amount': float(amount),
            'category': category,
            'category_encoded': self.categories.get(category, 7),
            'description': description,
            'date': now.strftime("%Y-%m-%d %H:%M:%S"),
            'day_of_week': now.weekday(),
            'month': now.month,
            'is_weekend': now.weekday() >= 5,
            'year': now.year
        }
        
        self.transactions.append(transaction)
        self.save_data()
        
        # Ré-entraînement périodique
        if len(self.transactions) % 10 == 0:
            self.train_model()
        
        return transaction
    
    def train_model(self):
        """Entraîne le modèle de réseau de neurones"""
        if len(self.transactions) < 20:
            return
        
        X, y = FinancialDataProcessor.prepare_training_data(self.transactions)
        if X is not None:
            self.network.train(X, y, epochs=500)
    
    def predict_next_week(self):
        """Prédit les dépenses pour la semaine prochaine"""
        if len(self.transactions) < 7:
            return None
        
        # Préparer les dernières données
        recent_data = self.transactions[-7:]
        amounts = [t['amount'] for t in recent_data]
        days_of_week = [t['day_of_week'] for t in recent_data]
        
        max_amount = max(abs(a) for a in amounts) if max(abs(a) for a in amounts) > 0 else 1
        normalized_amounts = [a / max_amount for a in amounts]
        
        # Créer le vecteur d'entrée
        input_vector = normalized_amounts + [
            days_of_week[-1] / 7,
            recent_data[-1]['month'] / 12,
            1 if recent_data[-1]['is_weekend'] else 0,
            recent_data[-1]['category_encoded'] / 10
        ]
        
        # Faire la prédiction
        prediction = self.network.predict(np.array([input_vector]))[0][0]
        
        # Dénormaliser
        prediction = prediction * max_amount
        
        return {
            'predicted_amount': float(prediction),
            'confidence': 0.85,
            'next_7_days': self._generate_weekly_forecast(prediction)
        }
    
    def _generate_weekly_forecast(self, base_amount):
        """Génère des prévisions pour les 7 prochains jours"""
        forecast = []
        today = datetime.now()
        
        for i in range(1, 8):
            day = today + timedelta(days=i)
            # Variation aléatoire basée sur le jour de la semaine
            if day.weekday() >= 5:  # Weekend
                variation = 1.3  + np.random.normal(0, 0.1)
            else:
                variation = 1.0 + np.random.normal(0, 0.05)
            
            forecast.append({
                'date': day.strftime("%Y-%m-%d"),
                'day': day.strftime("%A"),
                'predicted_amount': float(base_amount * variation),
                'is_weekend': day.weekday() >= 5
            })
        
        return forecast
    
    def get_spending_analysis(self):
        """Analyse des dépenses"""
        if not self.transactions:
            return {}
        
        analysis = {
            'total_spent': sum(t['amount'] for t in self.transactions if t['amount'] < 0),
            'total_income': sum(t['amount'] for t in self.transactions if t['amount'] > 0),
            'by_category': {},
            'monthly_trend': [],
            'alerts': []
        }
        
        # Analyse par catégorie
        for category in self.categories:
            cat_amount = sum(t['amount'] for t in self.transactions 
                           if t.get('category') == category and t['amount'] < 0)
            if cat_amount < 0:
                analysis['by_category'][category] = {
                    'amount': abs(cat_amount),
                    'percentage': abs(cat_amount) / abs(analysis['total_spent']) * 100
                }
                
                # Vérifier les budgets
                if abs(cat_amount) > self.budgets.get(category, 0):
                    analysis['alerts'].append({
                        'type': 'budget_exceeded',
                        'category': category,
                        'spent': abs(cat_amount),
                        'budget': self.budgets[category]
                    })
        
        # Tendance mensuelle
        monthly_data = {}
        for transaction in self.transactions:
            month_key = f"{transaction['year']}-{transaction['month']:02d}"
            if month_key not in monthly_data:
                monthly_data[month_key] = 0
            monthly_data[month_key] += transaction['amount']
        
        analysis['monthly_trend'] = [
            {'month': month, 'amount': amount} 
            for month, amount in sorted(monthly_data.items())
        ]
        
        # Alertes intelligentes
        if analysis['total_spent'] < -1000:
            analysis['alerts'].append({
                'type': 'high_spending',
                'message': 'Vos dépenses sont élevées ce mois-ci'
            })
        
        return analysis
    
    def get_savings_recommendations(self):
        """Génère des recommandations d'épargne"""
        analysis = self.get_spending_analysis()
        recommendations = []
        
        if analysis.get('total_income', 0) > 0:
            savings_rate = abs(analysis.get('total_spent', 0)) / analysis['total_income']
            
            if savings_rate > 0.8:
                recommendations.append({
                    'type': 'critical',
                    'title': 'Réduisez vos dépenses',
                    'message': f'Vous dépensez {savings_rate*100:.1f}% de vos revenus'
                })
            
            # Identifier les catégories avec plus de dépenses
            if analysis.get('by_category'):
                top_category = max(analysis['by_category'].items(), 
                                 key=lambda x: x[1]['amount'], 
                                 default=(None, {'amount': 0}))
                
                if top_category[0]:
                    recommendations.append({
                        'type': 'suggestion',
                        'title': 'Optimisation des dépenses',
                        'message': f'Pensez à réduire vos dépenses en {top_category[0]}'
                    })
        
        # Recommandation générale d'épargne
        if analysis.get('total_income', 0) > 2000:
            recommendations.append({
                'type': 'savings',
                'title': 'Épargnez 20%',
                'message': 'Essayez d\'épargner au moins 20% de vos revenus'
            })
        
        return recommendations

# Instance globale de l'assistant financier
FINANCIAL_ASSISTANT = FinancialAssistant()