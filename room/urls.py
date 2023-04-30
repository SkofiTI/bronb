from django.urls import path

from .views import *


urlpatterns = [
    path('', rooms_list, name='rooms_list_url'),
    path('profile/', profile, name='profile_url'),
    path('room/<str:slug>/', room_detail, name='room_detail_url')
]