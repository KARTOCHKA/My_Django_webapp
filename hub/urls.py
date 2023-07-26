from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('calculator/', views.calculator, name='calculator'),
    path('chat/', views.chat_with_gpt, name='chat_with_gpt'),
    path('register/', views.register, name='register'),
]

