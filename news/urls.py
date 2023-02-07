from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.NewsView.as_view(), name='news'),
    path('crypto/', views.CryptoNewsView.as_view(), name='crypto_news'),
    path('twitter/', views.TwitterView.as_view(), name='twitter'),
    path('websites/', views.websites, name='websites'),

    ]



