from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Room, Day, BookingDate, Booking


def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'room/pages/rooms.html', context={'rooms': rooms})


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
        return render(request, 'room/pages/profile.html', context={'bookings': bookings})


@login_required
def bronb_list(request, slug, date, start_time, end_time, room_title):
    room = get_object_or_404(Room, slug=slug)
    day = get_object_or_404(Day, date=date, month__room=room)
    booking_date = get_object_or_404(BookingDate, start_time=start_time, end_time=end_time, day_id=day.id)

    booking_date.is_available = False
    booking_date.save()

    Booking.objects.create(user=request.user, room=room, booking_date=booking_date)

    return redirect('rooms_list_url')


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.cancel_booking()

    return redirect('profile_url')


@user_passes_test(lambda u: u.is_superuser)
def change_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    new_status = request.POST.get('status')
    booking.change_status(new_status)

    return redirect('admin_panel_url')


@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    bookings = Booking.objects.all()

    return render(request, 'room/pages/admin_panel.html', context={'bookings': bookings})