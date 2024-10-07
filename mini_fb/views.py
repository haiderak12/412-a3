from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Profile # import the models

# class-based view
class ShowAllProfilesView(ListView):
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template