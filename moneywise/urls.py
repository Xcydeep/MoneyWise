"""
URL configuration for moneywise project.
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Pages principales
    path('', views.home, name='home'),
    
    # API endpoints
    path('api/transaction/add', views.api_add_transaction, name='add_transaction'),
    path('api/predict', views.api_predict, name='predict'),
    path('api/analysis', views.api_analysis, name='analysis'),
    path('api/train', views.api_train_model, name='train_model'),
    path('api/recommendations', views.api_recommendations, name='recommendations'),
    path('api/budget/set', views.api_set_budget, name='set_budget'),
    path('api/transactions', views.api_transactions, name='transactions'),
    path('api/statistics', views.api_statistics, name='statistics'),
    path('api/weekly-report', views.api_weekly_report, name='weekly_report'),
    path('api/health', views.api_health, name='health'),
    
    # Démonstration
    path('demo/add-sample-data', views.demo_add_sample_data, name='add_sample_data'),
    path('demo/reset', views.reset_data, name='reset_data'),
]

