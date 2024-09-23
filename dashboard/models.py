from django.db import models

# Create your models here.
class coins(models.Model):
    name=models.TextField(max_length=20)
    details=models.TextField(max_length=500)