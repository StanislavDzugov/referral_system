from django.urls import path
from user_profile import views


urlpatterns = [
    path('', views.register_view, name='register'),
    path('confirmation/<str:pk>/', views.phone_confirmation_view, name='confirmation'),
    path('logout/', views.userlogout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]