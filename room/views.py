from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import Room, Day, BookingDate, Booking


def error_404(request, exception):
    return render(request, 'room/pages/404.html')


def rooms_list(request):
    rooms = Room.objects.all()

    return render(
        request,
        'room/pages/rooms.html',
        context={
            'rooms': rooms,
            'active_page': 'rooms_list',
        }
    )


def room_detail(request, slug):
    room = get_object_or_404(Room, slug__iexact=slug)
    return render(request, 'room/pages/room_detail.html', context={'room': room})


def profile(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    elif request.user.is_staff:
        return redirect('admin_panel_url')
    else:
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'room/pages/profile.html', context={'bookings': bookings, 'active_page': 'profile'})


@login_required
def bronb_list(request, slug, date, start_time, end_time, room_title):
    room = get_object_or_404(Room, slug=slug)
    day = get_object_or_404(Day, date=date, month__room=room)
    booking_date = get_object_or_404(BookingDate, start_time=start_time, end_time=end_time, day_id=day.id)

    Booking.objects.create(user=request.user, room=room, booking_date=booking_date)

    return redirect('rooms_list_url')


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.cancel_booking()

    return redirect('profile_url')


def change_booking_status(request, booking_id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseNotFound(render_to_string('room/pages/404.html'))
    booking = get_object_or_404(Booking, id=booking_id)
    new_status = request.POST.get('status')
    booking.change_status(new_status)

    if new_status == 'Одобрено':
        Booking.objects.filter(
            room=booking.room,
            booking_date=booking.booking_date,
        ).exclude(id=booking.id).update(status='Отклонено')

    return redirect('admin_panel_url')


def admin_panel(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseNotFound(render_to_string('room/pages/404.html'))
    bookings = Booking.objects.all()

    return render(request, 'room/pages/admin_panel.html', context={'bookings': bookings, 'active_page': 'profile'})