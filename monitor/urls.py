from .views import *
from django.contrib.auth.decorators import login_required
from django.urls import path


app_name = 'monitor'
urlpatterns = [
    path('watchlist', login_required(WatchlistView.as_view()), name='watchlist'),
    path('portfolio', login_required(PortfolioView.as_view()), name='portfolio'),
    path('alerts', login_required(AlertsView.as_view()), name='alerts'),
    path('screener', login_required(ScreenerView.as_view()), name='screener'),
    path('twitter/<str:query>', login_required(TwitterView.as_view()), name='twitter'),
    ]
