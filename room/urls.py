from django.urls import path

from .views import *


urlpatterns = [
    path('', rooms_list, name='rooms_list_url'),
    path('profile/', profile, name='profile_url'),
    path('admin_panel/', admin_panel, name='admin_panel_url'),
    path('room/<str:slug>/', room_detail, name='room_detail_url'),
    path('room/<str:slug>/bronb/<str:room_title>/<str:date>/<str:start_time>/<str:end_time>/', bronb_list, name='bronb_list_url'),
    path('profile/<int:booking_id>/cancel/', cancel_booking, name='cancel_booking_url'),
    path('profile/<int:booking_id>/change_status/', change_booking_status, name='change_booking_status_url'),
]