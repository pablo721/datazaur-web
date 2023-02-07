from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'trade'
urlpatterns = [
    path('', views.TradeView.as_view(), name='trade'),
    path('momentum/', views.MomentumView.as_view(), name='momentum'),
    path('arbitrage/', views.ArbitrageView.as_view(), name='arbitrage'),
    path('stat_arb/', views.StatArbView.as_view(), name='stat_arb'),
    path('signals/', views.SignalsView.as_view(), name='signals'),
    path('insider_trades/', views.InsiderTradesView.as_view(), name='insider_trades'),
    ]



