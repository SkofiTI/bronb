from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import redirect_room


urlpatterns = [
    path('', redirect_room),
    path('admin/', admin.site.urls),
    path('rooms/', include('room.urls')),
    path('auth/', include('authentication.urls'))
]


handler404 = 'room.views.error_404'