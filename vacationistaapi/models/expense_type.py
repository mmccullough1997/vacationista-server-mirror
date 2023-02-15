from django.db import models

class ExpenseType(models.Model):
  label = models.CharField(max_length=50)
