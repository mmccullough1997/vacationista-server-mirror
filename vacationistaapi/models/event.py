from django.db import models
from .event_type import EventType
from .trip import Trip
from .leg import Leg

class Event(models.Model):
  event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
  leg = models.ForeignKey(Leg, on_delete=models.CASCADE)
  description = models.CharField(max_length=500)
  location = models.CharField(max_length=500)
  date = models.DateField(blank=True, null=True)
  image = models.CharField(max_length=500, blank=True, null=True)
  title = models.CharField(max_length=500)
