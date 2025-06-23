from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_trade, name='log_trade'),
    path('history/', views.trade_history, name='trade_history'),
]
