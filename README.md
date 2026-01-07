# MoneyWise - Assistant Financier Intelligent

## Description

MoneyWise est une application web Django innovante qui intègre des réseaux de neurones artificiels pour transformer la gestion financière personnelle en une expérience intelligente, proactive et personnalisée. L'application permet aux utilisateurs de suivre leurs transactions, d'analyser leurs dépenses, de prédire leurs besoins budgétaires futurs et de recevoir des recommandations personnalisées basées sur l'intelligence artificielle.

## Fonctionnalités Principales

### Gestion des Transactions
- Ajout manuel des transactions financières (revenus et dépenses)
- Catégorisation automatique des transactions à l'aide de réseaux de neurones
- Historique complet des transactions avec recherche et filtrage

### Analyse Intelligente
- Analyse des tendances de dépenses par catégorie
- Détection d'anomalies et d'alertes budgétaires
- Statistiques détaillées (revenus moyens, dépenses moyennes, taux d'épargne)

### Prédictions avec IA
- Prédiction des dépenses pour les 7 prochains jours
- Modèle de réseau de neurones entraîné sur les données personnelles
- Prévisions ajustées selon les jours de la semaine et les saisons

### Recommandations Personnalisées
- Conseils d'épargne basés sur les habitudes de consommation
- Alertes de dépassement de budget par catégorie
- Suggestions d'optimisation financière

### Interface Web
- Dashboard interactif avec graphiques et visualisations
- Interface responsive et intuitive
- API REST complète pour intégrations externes

## Architecture Technique

- **Framework** : Django 4.0+
- **Base de données** : SQLite (facilement remplaçable par PostgreSQL/MySQL)
- **IA/ML** : Réseaux de neurones implémentés avec NumPy
- **Frontend** : Templates Django avec HTML/CSS/JavaScript
- **Cache** : Système de cache Django pour la persistance des données

## Prérequis

- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)
- Navigateur web moderne

## Installation et Configuration

### 1. Installation des Dépendances

Assurez-vous d'avoir Python installé, puis exécutez :

```bash
pip install django numpy
```

### 2. Configuration du Projet

Le projet est prêt à l'emploi avec la configuration par défaut :
- Base de données SQLite (`db.sqlite3`)
- Serveur de développement Django
- Templates dans le dossier `templates/`
- Fichiers statiques dans `static/`

### 3. Migration de la Base de Données

Bien que le projet utilise principalement le cache Django pour la persistance, exécutez les migrations si nécessaire :

```bash
python manage.py migrate
```

## Lancement de l'Application

Pour démarrer le serveur de développement Django :

```bash
python manage.py runserver
```

L'application sera accessible dans votre navigateur à l'adresse :
**http://127.0.0.1:8000/**

Le serveur se lance par défaut sur le port 8000. Vous pouvez spécifier un port différent :

```bash
python manage.py runserver 8080
```

## Utilisation

### Interface Web
1. Accédez à la page d'accueil pour voir le dashboard
2. Ajoutez des transactions via l'interface ou l'API
3. Consultez les analyses et prédictions en temps réel
4. Recevez des recommandations personnalisées

### API REST
L'application expose une API complète. Voici les endpoints principaux :

- `GET /` - Page d'accueil avec dashboard
- `POST /api/transaction/add` - Ajouter une transaction
- `GET /api/predict` - Obtenir des prédictions IA
- `GET /api/analysis` - Analyse des dépenses
- `GET /api/recommendations` - Recommandations d'épargne
- `POST /api/budget/set` - Définir un budget par catégorie
- `GET /api/statistics` - Statistiques détaillées
- `GET /api/health` - État de santé du système

### Données de Démonstration
Pour tester l'application avec des données exemples :
- Accédez à `/demo/add-sample-data` pour ajouter des transactions de démonstration
- Le modèle IA s'entraînera automatiquement sur ces données

## Structure du Projet

```
moneywise/
├── manage.py                 # Script de gestion Django
├── moneywise/               # Configuration principale
│   ├── settings.py          # Paramètres Django + logique IA
│   ├── urls.py              # Configuration des URLs
│   ├── views.py             # Vues et API
│   └── ...
├── core/                    # Application Django
├── templates/               # Templates HTML
├── static/                  # Fichiers statiques
└── db.sqlite3              # Base de données
```

## Développement et Extension

### Entraînement du Modèle IA
Le modèle de réseau de neurones s'entraîne automatiquement toutes les 10 transactions. Vous pouvez forcer l'entraînement via l'API :

```bash
curl -X POST http://127.0.0.1:8000/api/train
```

### Personnalisation
- Modifiez les catégories dans `settings.py`
- Ajustez les paramètres du réseau de neurones
- Étendez l'API avec de nouveaux endpoints
- Intégrez des sources de données externes (banques, etc.)

## Dépannage

### Problèmes Courants

1. **Erreur d'importation Django** :
   - Vérifiez que Django est installé : `pip list | grep django`
   - Activez votre environnement virtuel si utilisé

2. **Port déjà utilisé** :
   - Changez de port : `python manage.py runserver 8001`

3. **Permissions base de données** :
   - Assurez-vous que le fichier `db.sqlite3` est accessible en écriture

4. **Prédictions non disponibles** :
   - Ajoutez au moins 7 transactions pour activer les prédictions IA

### Logs et Debug
- Activez le mode debug dans `settings.py` pour plus d'informations
- Consultez les logs du serveur dans la console

## Sécurité

- L'application utilise les protections CSRF de Django
- Les données sensibles sont stockées localement (SQLite)
- Pour un déploiement en production, configurez un serveur web approprié (Nginx, Apache)

## Contribution

Ce projet est open-source. Pour contribuer :
1. Forkez le repository
2. Créez une branche pour vos modifications
3. Testez vos changements
4. Soumettez une pull request

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Support

Pour des questions ou des problèmes :
- Consultez la documentation dans `docuent.md`
- Vérifiez les logs d'erreur
- Ouvrez une issue sur le repository

---

**MoneyWise** - Votre assistant financier intelligent alimenté par l'IA.
