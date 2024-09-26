## formdata/urls.py
## description: URL patterns for the formdata app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.show_form, name="show_form"), ## new!
    path(r'submit', views.submit, name="submit")
]