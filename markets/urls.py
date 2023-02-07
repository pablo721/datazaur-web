from django.urls import path, include

from . import views


app_name = 'markets'
urlpatterns = [
    path('', views.MarketsView.as_view(), name='markets'),
    #path('trade/', include('trade.urls'), name='trade'),
    path('crypto/', include('crypto.urls'), name='crypto'),
    path('indices/', views.IndicesView.as_view(), name='indices'),
    path('commodities/', views.CommoditiesView.as_view(), name='commodities'),
    path('forex/', views.ForexView.as_view(), name='forex'),
    path('forex_matrix/', views.forex_matrix, name='forex_matrix'),
    path('bonds/', views.BondsView.as_view(), name='bonds'),
    path('stocks/', views.StocksView.as_view(), name='stocks'),
    path('funds/', views.FundsView.as_view(), name='funds'),
    path('etfs/', views.ETFView.as_view(), name='etfs'),
    path('yield_curves/', views.YieldCurvesView.as_view(), name='yield_curves'),
    path('screener/', views.ScreenerView.as_view(), name='screener'),
    path('sectors/', views.SectorsView.as_view(), name='sectors'),
    ]
