# mini_fb/models.py
# Definte the data objects for our application
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

# Create your models here.

class Profile(models.Model):
    
    # data attributes of a Profile
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''
        Return a string representation of this object.
        '''
        return f'{self.firstname} {self.lastname}'
    
    def get_status_messages(self):
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        friendships = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        friends = []
        for friendship in friendships:
            if friendship.profile1 == self:
                friends.append(friendship.profile2)
            else:
                friends.append(friendship.profile1)
        return friends
    
    def add_friend(self, other):
        if self == other:
            print("Cannot add yourself as a friend.")
            return

        friendship_exists = Friend.objects.filter(
            (Q(profile1=self) & Q(profile2=other)) | (Q(profile1=other) & Q(profile2=self))
        ).exists()

        if not friendship_exists:
            friendship = Friend(profile1=self, profile2=other)
            friendship.save()
            print(f"Friendship created between {self} and {other}.")
        else:
            print(f"Friendship already exists between {self} and {other}.")
    
    def get_friend_suggestions(self):
        all_profiles = Profile.objects.exclude(pk=self.pk)
        friends = self.get_friends()
        suggestions = all_profiles.exclude(pk__in=[friend.pk for friend in friends])
        return suggestions
    
    def get_news_feed(self):
        friends = self.get_friends()
        profiles = [self] + friends
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
        return news_feed
    
class StatusMessage(models.Model):

    # Data attributes of a StatusMessage
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_images(self):
        '''
        Returns all images associated with this object
        '''
        return self.image_set.all()
    
    def __str__(self):
        '''
        Return a string representation of the StatusMessage object
        '''
        return f"StatusMessage({self.profile.firstname} {self.profile.lastname} at {self.timestamp})"

class Image(models.Model):
    
    # Data attributes of an Image
    image_file = models.ImageField(upload_to='images/')
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        '''
        Returns a string representation of the Image Instance
        '''
        return f"Image for StatusMessage {self.status_message.id} at {self.timestamp}"

class Friend(models.Model):
    profile1 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friend_set1'
    )
    profile2 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='friend_set2'
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.firstname} {self.profile1.lastname} & {self.profile2.firstname} {self.profile2.lastname}"