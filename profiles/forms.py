from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from profiles.models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("username", "email")


class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ("username", "email")
