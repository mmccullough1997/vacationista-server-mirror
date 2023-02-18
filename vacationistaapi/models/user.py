from django.db import models

class User(models.Model):
  uid = models.CharField(max_length=50)
  first_name = models.CharField(max_length=25)
  last_name = models.CharField(max_length=25)
  date_registered = models.DateField()
  username = models.CharField(max_length=50)
  bio = models.CharField(max_length=400)
  image = models.CharField(max_length=200)
