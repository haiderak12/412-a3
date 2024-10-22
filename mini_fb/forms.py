from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name", required=True)
    lastname = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    message = forms.CharField(label="Message", required=True)

    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']