from django.urls import path

from profiles.views import ProfileView

app_name = "profiles"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
]
