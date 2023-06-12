from django.db import models
from django.shortcuts import reverse

from authentication.models import User


class Room(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    time = models.CharField(max_length=20)
    seats = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.title)
    
    def get_absolute_url(self):
        return reverse("room_detail_url", kwargs={"slug": self.slug})


class Month(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='months')
    name = models.CharField(max_length=10)


class Day(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='days')
    name = models.CharField(max_length=20)
    date = models.DateField()


class BookingDate(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='booking_dates')
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.ForeignKey(BookingDate, on_delete=models.CASCADE)

    status_choices = [
        ('Рассматривается', 'Рассматривается'),
        ('Одобрено', 'Одобрено'),
        ('Отклонено', 'Отклонено'),
    ]

    status = models.CharField(max_length=20, choices=status_choices, default='Рассматривается')

    def cancel_booking(self):
        self.booking_date.is_available = True
        self.booking_date.save()
        self.delete()


    def change_status(self, new_status):
        self.status = new_status

        if new_status == 'Отклонено':
            self.booking_date.is_available = True
            self.booking_date.save()

        self.save()