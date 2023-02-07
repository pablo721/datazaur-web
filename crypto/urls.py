from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'crypto'
urlpatterns = [
    path('', views.CryptoView.as_view(), name='crypto'),
    path('exchanges/', views.ExchangesView.as_view(), name='exchanges'),
    path('addExchange/', views.add_exchange, name='add_exchange'),
    path('dominance/', views.dominance, name='dominance'),
    path('global_metrics/', views.GlobalMetricsView.as_view(), name='global_metrics'),
    path('movers/', views.MoversView.as_view(), name='movers'),
    path('defi/', views.DeFiView.as_view(), name='defi'),
    path('nft/', views.NFTView.as_view(), name='nft'),
    path('change_currency/', views.crypto_change_currency, name='change_currency'),
    ]
