from django.db import models
from .user import User

class Leg(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start = models.DateField()
  end = models.DateField()
  location = models.CharField(max_length=500)
  budget = models.DecimalField(max_digits=20, decimal_places=2)
