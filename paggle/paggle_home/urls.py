from django.urls import path
from .views import (
    DatasetListView, 
    DatasetDetailView, 
    ModelCreateView
    )
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='paggle_home'),
    path('register/', user_views.register, name='register'),
    path('selectTask/', views.selectTask, name='paggle-selectTask'),
    path('selectData/', DatasetListView.as_view(), name='paggle-selectData'),
    path('selectData/<int:pk>/', DatasetDetailView.as_view(), name='selectData-detail'),
    path('createModel/new/', ModelCreateView.as_view(), name='paggle-createModel'),
    path('monitor/', views.monitor, name='paggle-monitor'),
    path('runModel/', views.runModel, name='paggle-runModel'),
]

# Looking for naming pattern of template -> <app>/<model>_<viewtype>.html