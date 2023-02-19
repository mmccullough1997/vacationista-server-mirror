from django.db import models

class Recommendation(models.Model):
  title = models.CharField(max_length=500)
  category = models.CharField(max_length=500)
  description = models.CharField(max_length=500, null=True, blank=True)
  location = models.CharField(max_length=500)
  rating = models.DecimalField(max_digits=20, decimal_places=2)
  image = models.CharField(max_length=500, null=True, blank=True)
