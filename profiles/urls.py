from allauth.socialaccount.providers.discord import views as discord_views
from django.urls import path

urlpatterns = [
    path("accounts/discord/login/", discord_views.oauth2_login, name="discord_login"),
    path(
        "accounts/discord/login/callback/",
        discord_views.oauth2_callback,
        name="discord_callback",
    ),
]
