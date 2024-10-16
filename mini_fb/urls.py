# mini_fb/urls.py
# description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path(r'create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
]