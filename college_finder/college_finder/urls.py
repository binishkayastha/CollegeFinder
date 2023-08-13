from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from sign_in import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign_in/', include(('sign_in.urls', 'sign_in'), namespace='sign_in')),
    path('colleges/', include(('colleges.urls', 'colleges'), namespace='colleges')),
    path('', views.home, name='home'),
]
