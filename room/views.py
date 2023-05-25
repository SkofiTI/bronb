from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from .models import Room


def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'room/pages/rooms.html', context={'rooms': rooms})


def room_detail(request, slug):
    room = get_object_or_404(Room, slug__iexact=slug)
    months = room.months.all()
    context = {
        'room': room,
        'months': months,
    }
    return render(request, 'room/pages/room_detail.html', context=context)


def profile(request):
    """ Обработчик для страницы личного кабинета
        TODO поменять навзание
    """
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        return render(request, 'room/pages/profile.html')