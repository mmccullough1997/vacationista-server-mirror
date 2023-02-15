from django.db import models

class TransportationType(models.Model):
  label = models.CharField(max_length=50)
