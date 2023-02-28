from django.db import models
from .user import User

class Trip(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start = models.DateField()
  end = models.DateField()
  travel_from = models.CharField(max_length=500)
  travel_to = models.CharField(max_length=500)
  budget = models.DecimalField(max_digits=20, decimal_places=2)

  @property
  def duration(self):
    return self.__duration
  
  @duration.setter
  def duration(self, value):
    self.__duration = value

  @property
  def events(self):
    return self.__events
  
  @events.setter
  def events(self, value):
    self.__events = value
    
  @property
  def legs(self):
    return self.__legs
  
  @legs.setter
  def legs(self, value):
    self.__legs = value
