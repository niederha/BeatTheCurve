from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signUp, name="signup"),
    path('signin', views.signIn, name="signin"),
    path('customsignup', views.customSignUp, name="customsignup"),
    path('dashboard', views.dashboard, name="dashboard")
]
