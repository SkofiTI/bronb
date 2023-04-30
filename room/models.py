from django.db import models
from django.shortcuts import reverse


class Room(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    time = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.title)
    
    def get_absolute_url(self):
        return reverse("room_detail_url", kwargs={"slug": self.slug})


class RoomDetail(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    seats = models.IntegerField()
