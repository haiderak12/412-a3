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
    path(r'profile/<int:pk>/update_profile', views.UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/<int:pk>/delete_status', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/<int:pk>/update_status', views.UpdateStatusMessageView.as_view(), name='update_status'),
]