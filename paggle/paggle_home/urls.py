from django.urls import path
from .views import DatasetListView, DatasetDetailView
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='paggle_home'),
    path('register/', user_views.register, name='register'),
    path('selectTask/', views.selectTask, name='paggle-selectTask'),
    path('selectData/', DatasetListView.as_view(), name='paggle-selectData'),
    path('selectData/<int:pk>/', DatasetDetailView.as_view(), name='selectData-detail'),
    path('selectModel/', views.selectModel, name='paggle-selectModel'),
    path('monitor/', views.monitor, name='paggle-monitor'),
]

# Looking for naming pattern of template -> <app>/<model>_<viewtype>.html