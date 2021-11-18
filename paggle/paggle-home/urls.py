from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='paggle-home'),
    path('selectData/', views.selectData, name='paggle-selectData'),
    path('login/', views.login, name='paggle-login'),
    path('register/', views.register, name='paggle-register'),
    path('monitor/', views.monitor, name='paggle-monitor'),
]