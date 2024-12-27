from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from users.models import UserRoles
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('No superuser found. Creating one...'))
            User.objects.create_superuser(
                username=os.environ.get('ADMIN_USERNAME', 'admin'),
                email=os.environ.get('ADMIN_EMAIL', 'admin@gmail.com'),
                password=os.environ.get('ADMIN_PASSWORD', 'yourpassword'),
                role=UserRoles.BOSS
            )
        else:
            self.stdout.write(self.style.WARNING('A superuser already exists.'))
