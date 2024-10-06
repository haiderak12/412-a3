# mini_fb/models.py
# Definte the data objects for our application
from django.db import models

# Create your models here.

class Profile(models.Model):
    
    # data attributes of a Profile
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this object.'''

        return f'{self.firstname} {self.lastname}' 