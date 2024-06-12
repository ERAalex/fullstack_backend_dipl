from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        print('---1--1--1--')
        User = get_user_model()
        if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
            User.objects.create_superuser(
                username=os.environ['DJANGO_SUPERUSER_USERNAME'],
                email=os.environ['DJANGO_SUPERUSER_EMAIL'],
                password=os.environ['DJANGO_SUPERUSER_PASSWORD']
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
