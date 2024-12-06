from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('manage_bookings/<int:tour_id>/', views.manage_bookings, name='manage_bookings'),
    path('user_info/', views.user_info, name='user_info'),
    path('user_bookings/', views.user_bookings, name='user_bookings'),
]
