from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.forms import ProfileChangeForm, ProfileCreationForm
from profiles.models import Profile


class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile
    list_display = ("email", "username")


admin.site.register(Profile, ProfileAdmin)
