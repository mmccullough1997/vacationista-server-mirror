from django.db import models

class Highlight(models.Model):
  title = models.CharField(max_length=50)
  content = models.CharField(max_length=500)
  image = models.CharField(max_length=500)
  location = models.CharField(max_length=500)
  thumbnail = models.CharField(max_length=500)
