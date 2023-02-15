from django.db import models
from .expense_type import ExpenseType
from .trip import Trip
from .leg import Leg

class Expense(models.Model):
  expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
  trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
  leg = models.ForeignKey(Leg, on_delete=models.CASCADE, null=True, blank=True)
  amount = models.DecimalField(max_digits=20, decimal_places=2)
  comment = models.CharField(max_length=500)
  title = models.CharField(max_length=500)
  