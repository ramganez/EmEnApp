from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=2)
    designation = models.CharField(max_length=150)

    def get_absolute_url(self):

        return reverse('profile', kwargs={'username_id': self.user.username.split('@')[0]+"_"+str(self.user.id)})
