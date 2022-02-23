from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin

from allauth.socialaccount.signals import social_account_updated
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.dispatch import receiver


@receiver(social_account_updated)
def make_admin(request: WSGIRequest, sociallogin: "SocialLogin", **kwargs):
    """Make the user admin if they are logging in via discord, and their discord UID
    matches the one provided via the environmental variable DISCORD_BOOTSTRAP_ADMIN_UID.
    """
    if (
        settings.DISCORD_BOOTSTRAP_ADMIN_UID is not None
        and sociallogin.account.provider == "discord"
        and settings.DISCORD_BOOTSTRAP_ADMIN_UID == sociallogin.account.uid
        and (
            sociallogin.user.is_superuser is not True
            or sociallogin.user.is_staff is not True
        )
    ):
        sociallogin.user.is_superuser = True
        sociallogin.user.is_staff = True
        sociallogin.user.save()
