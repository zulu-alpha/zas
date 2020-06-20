from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.conf import settings


class Command(BaseCommand):
    help = "For creating an initial admin on a fresh DB with no user input."

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.all():
            raise CommandError("Bootstrap error: There is already at least one user!")
        if None in settings.BOOTSTRAP_ADMIN.values():
            raise CommandError("Bootstrap error: Not all boostrap user details provided!")
        admin = User.objects.create_superuser(
            settings.BOOTSTRAP_ADMIN["USERNAME"],
            settings.BOOTSTRAP_ADMIN["EMAIL"],
            settings.BOOTSTRAP_ADMIN["PASSWORD"]
        )
        self.stdout.write(f"Created superuser {admin}")
