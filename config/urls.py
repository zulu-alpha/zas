"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import LogoutView
from allauth.socialaccount.providers.discord import views as discord_views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from profiles.views import HomeView

allauth = [
    path("discord/login/", discord_views.oauth2_login, name="discord_login"),
    path(
        "discord/login/callback/",
        discord_views.oauth2_callback,
        name="discord_callback",
    ),
    path("logout/", LogoutView.as_view(), name="account_logout"),
]

debug_toolbar = [
    path("__debug__/", include("debug_toolbar.urls")),
]

home_page = [path("", HomeView.as_view())]


apps = [
    path("admin/", admin.site.urls),
    path("profiles/", include("profiles.urls", "profiles")),
]

urlpatterns = allauth + debug_toolbar + home_page + apps
