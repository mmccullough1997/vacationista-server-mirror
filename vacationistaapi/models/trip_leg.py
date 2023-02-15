from django.db import models
from .trip import Trip
from .leg import Leg

class TripLeg(models.Model):
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
  leg = models.ForeignKey(Leg, on_delete=models.CASCADE)
