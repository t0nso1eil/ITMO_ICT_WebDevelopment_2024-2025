from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CarsDeleteView, CarsList, CarRetrieveView, CarUpdateView, CarCreateView, CarDeleteView

urlpatterns = [
    path('owner/<int:owner_id>/', views.get_owner, name='owner_detail'),
    path('owners/', views.get_all_owners),
    path('cars/', CarsList.as_view()),
    path('cars/<int:pk>/', CarRetrieveView.as_view()),
    path('cars/<int:pk>/update/', CarUpdateView.as_view()),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view()),
    path('cars/delete/', CarsDeleteView),
    path('cars/create/', CarCreateView.as_view()),
    path('owners/create', views.create_owner)
]