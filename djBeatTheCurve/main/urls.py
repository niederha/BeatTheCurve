from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signUp, name="signup"),
    path('signin', views.signIn, name="signin"),
    path('customsignup', views.customSignUp, name="customsignup"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('daily', views.daily, name="daily"),
    path('quiz', views.quiz, name="quiz"),
    path('situation', views.situation, name="situation"),
    path('simulation', views.simulation, name="simulation")   
]
