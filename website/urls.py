from django.urls import path
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('log_out', views.LogoutView.as_view(), name='log_out'),
    ]
