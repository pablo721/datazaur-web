from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'calendar_'
urlpatterns = [
    path('macro/', views.MacroCalendarView.as_view(), name='macro_calendar'),
    path('crypto/', views.CryptoCalendarView.as_view(), name='crypto_calendar'),
    path('ipo/', views.IPOCalendarView.as_view(), name='ipo_calendar'),
    path('earnings/', views.EarningsCalendarView.as_view(), name='earnings_calendar'),
    ]

