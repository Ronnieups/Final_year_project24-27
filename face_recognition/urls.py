from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register_pickup_person/', views.register_pickup_person, name='register_pickup_person'),
    path('register_face/', views.register_face, name='register_face'),
    path('pickup_schedule/', views.pickup_schedule, name='pickup_schedule'),
]