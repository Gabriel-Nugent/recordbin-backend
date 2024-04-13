"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profile/', Profile.as_view(), name='profile_api'),
    path('search-artist/', search_artist, name='search_artist'),
    path('search-release/', search_release, name='search_release'),
    path('get-artist/', get_artist, name='get_artist'),
    path('get-release/', get_release, name='get_release'),
    path('releases-by-artist/', releases_by_artist, name='releases_by_artist'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('create-list/', CreateList.as_view(), name='create_list'),

]