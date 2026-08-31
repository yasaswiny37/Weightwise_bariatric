from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('module/<int:pk>/', views.module_detail_view, name='module_detail'),
]
