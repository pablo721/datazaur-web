from rest_framework import routers
from . import views


router2 = routers.DefaultRouter()
router2.register('watchlist', views.WatchlistViewSet, basename='watchlist')
router2.register('crypto_ticker', views.CryptoTickerViewSet, basename='crypto_ticker')

