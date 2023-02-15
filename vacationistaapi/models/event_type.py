from django.db import models

class EventType(models.Model):
  label = models.CharField(max_length=50)
