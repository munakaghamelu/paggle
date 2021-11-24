from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='paggle-home'),
    path('selectTask/', views.selectTask, name='paggle-selectTask'),
    path('selectData/', views.selectData, name='paggle-selectData'),
    path('selectModel/', views.selectModel, name='paggle-selectModel'),
    path('monitor/', views.monitor, name='paggle-monitor'),
]