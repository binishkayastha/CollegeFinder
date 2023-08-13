from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('add/', views.add_college, name='add'),
    path('apply/<str:pk>/', views.apply_to_college, name='apply_to_college'),
]
