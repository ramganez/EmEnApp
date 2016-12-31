from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    years_of_experience = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    designation = models.CharField(max_length=150)

