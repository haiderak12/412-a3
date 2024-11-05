# mini_fb/urls.py
# description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

# all of the URLs that are part of this app
urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/', ShowProfileSelfView.as_view(), name='show_profile_self'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name='news_feed'),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('status/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/create', CreateProfileView.as_view(), name='create_profile'),
    # Login and Logout URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]