from django.urls import path, include
from . import views


app_name = 'macro'
urlpatterns = [
    path('', views.MacroView.as_view(), name='macro'),
    path('inflation/', views.InflationView.as_view(), name='inflation'),
    path('debt/', views.DebtView.as_view(), name='debt'),
    path('gdp/', views.GDPView.as_view(), name='gdp'),
    ]
