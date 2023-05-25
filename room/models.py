from django.db import models
from django.shortcuts import reverse


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
    start_time = models.TimeField()
    end_time = models.TimeField()