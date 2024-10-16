from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile # import the models
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

# class-based view
class ShowAllProfilesView(ListView):
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['status_messages'] = profile.get_status_messages()
        return context

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        profile_pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': profile_pk})