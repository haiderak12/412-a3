from django.shortcuts import render

# Create your views here.
from django.views.generic import *
from .models import * # import the models
from .forms import *
from django.urls import reverse
from django.shortcuts import redirect

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
        # Attach the profile to the status message
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        form.instance.profile = profile

        # Save the status message to the database
        sm = form.save()

        # Read the files from the request
        files = self.request.FILES.getlist('files')
        print(f"Number of files uploaded: {len(files)}")  # Debugging statement

        # Iterate over each file and create an Image object
        for f in files:
            # Create an Image object but don't save to the database yet
            image = Image()
            image.image_file = f
            image.status_message = sm
            
            # Save the Image object to the database
            image.save()
            print(f"Saved image: {image.image_file.name}")  # Debugging statement

        return super().form_valid(form)
    
    def get_success_url(self):
        profile_pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': profile_pk})

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        profile_pk = self.object.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile_pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')

        try:
            profile = Profile.objects.get(pk=profile_pk)
            other_profile = Profile.objects.get(pk=other_pk)
        except Profile.DoesNotExist:
            return redirect('show_all_profiles')

        profile.add_friend(other_profile)

        return redirect(reverse('show_profile', kwargs={'pk': profile_pk}))

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context