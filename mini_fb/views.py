from django.shortcuts import render

# Create your views here.
from django.views.generic import *
from .models import * # import the models
from .forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# class-based view
class ShowAllProfilesView(ListView):
    """
    Display a list of all profiles.
    """
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template

class ShowProfilePageView(DetailView):
    """
    Display a single profile page.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class ShowProfileSelfView(LoginRequiredMixin, DetailView):
    """
    Display the profile page of the logged-in user.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    

    def get_object(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            return profile
        except Profile.DoesNotExist:
            # Redirect to create profile if it doesn't exist
            return redirect('create_profile')

class CreateProfileView(CreateView):
    """
    Allow users to create a new profile and user account.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        # Reconstruct both forms from POST data
        self.object = None
        form = self.get_form()
        user_form = UserCreationForm(self.request.POST)

        if form.is_valid() and user_form.is_valid():
            return self.form_valid(form, user_form)
        else:
            return self.form_invalid(form, user_form)

    def form_valid(self, form, user_form):
        # Save the user form and get the new user
        user = user_form.save()
        # Attach the user to the profile instance
        form.instance.user = user
        # Save the profile form
        self.object = form.save()
        # Log the user in
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form, user_form):
        # Re-render the page with the forms and errors
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form)
        )

    def get_success_url(self):
        return reverse('show_profile_self')
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    Allow profile owners to update their profile.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    

    def get_object(self):
        # Retrieve the profile associated with the logged-in user
        try:
            profile = Profile.objects.get(user=self.request.user)
            return profile
        except Profile.DoesNotExist:
            # Redirect to create profile if it doesn't exist
            return redirect('create_profile')

    def get_success_url(self):
        return reverse('show_profile_self')

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """
    Allow profile owners to post a status message.
    """
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        # Attach the profile to the status message
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile

        # Save the status message to the database
        sm = form.save()

        # Handle uploaded images
        files = self.request.FILES.getlist('files')
        for f in files:
            image = Image()
            image.image_file = f
            image.status_message = sm
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile_self')

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """
    Allow profile owners to delete their status messages.
    """
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'
    

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        profile = Profile.objects.get(user=request.user)
        # Check if the status message belongs to the user's profile
        if status_message.profile != profile:
            return redirect('show_profile_self')
        return super(DeleteStatusMessageView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('show_profile_self')

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """
    Allow profile owners to update their status messages.
    """
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'
    

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        profile = Profile.objects.get(user=request.user)
        # Check if the status message belongs to the user's profile
        if status_message.profile != profile:
            return redirect('show_profile_self')
        return super(UpdateStatusMessageView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('show_profile_self')

class CreateFriendView(LoginRequiredMixin, View):
    """
    Allow profile owners to add friends.
    """
    

    def dispatch(self, request, *args, **kwargs):
        other_pk = kwargs.get('other_pk')
        try:
            profile = Profile.objects.get(user=request.user)
            other_profile = Profile.objects.get(pk=other_pk)
        except Profile.DoesNotExist:
            return redirect('show_all_profiles')

        profile.add_friend(other_profile)
        return redirect('show_profile_self')

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """
    Display friend suggestions for the profile owner.
    """
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    

    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """
    Display the news feed for the profile owner.
    """
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    

    def get_object(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context