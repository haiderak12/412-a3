# mini_fb/models.py
# Definte the data objects for our application
from django.db import models
from django.utils import timezone
from django.urls import reverse

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
    
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"StatusMessage({self.profile.firstname} {self.profile.lastname} at {self.timestamp})"