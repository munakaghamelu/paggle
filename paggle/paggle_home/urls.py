from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='paggle_home'),
    path('register/', user_views.register, name='register'),
    path('selectTask/', views.selectTask, name='paggle-selectTask'),
    path('selectData/', views.selectData, name='paggle-selectData'),
    path('selectModel/', views.selectModel, name='paggle-selectModel'),
    path('monitor/', views.monitor, name='paggle-monitor'),
]