from django.db import models
from .user import User

class Leg(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start = models.DateField()
  end = models.DateField()
  location = models.CharField(max_length=500)
  budget = models.DecimalField(max_digits=20, decimal_places=2)

  @property
  def events(self):
    return self.__events
  
  @events.setter
  def events(self, value):
    self.__events = value

  @property
  def duration(self):
    return self.__duration
  
  @duration.setter
  def duration(self, value):
    self.__duration = value

  @property
  def trip(self):
    return self.__trip
  
  @trip.setter
  def trip(self, value):
    self.__trip = value

  @property
  def expenses(self):
    return self.__expenses

  @expenses.setter
  def expenses(self, value):
    self.__expenses = value

  @property
  def expense_total(self):
    return self.__expense_total

  @expense_total.setter
  def expense_total(self, value):
    self.__expense_total = value
    
  @property
  def transportations(self):
    return self.__transportations

  @transportations.setter
  def transportations(self, value):
    self.__transportations = value

  @property
  def transportation_total(self):
    return self.__transportation_total

  @transportation_total.setter
  def transportation_total(self, value):
    self.__transportation_total = value

  @property
  def total(self):
    return self.__total

  @total.setter
  def total(self, value):
    self.__total = value
