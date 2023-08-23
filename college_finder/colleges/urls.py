from django.urls import path
from . import views

urlpatterns = [
    path('',views.colleges,name='colleges'),
    path('search/', views.search, name='search'),
    path('add/', views.add_college, name='add'),
    path('edit/<str:pk>/',views.edit_college,name='edit_college'),
    path('delete/<str:pk>/',views.delete_college,name='delete_college'),
    path('apply/<str:pk>/', views.apply_to_college, name='apply_to_college'),
]
