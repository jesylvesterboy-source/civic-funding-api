from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser for production'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='Jeremiah').exists():
            User.objects.create_superuser(
                'Jeremiah', 
                'jesylvesterboy@gmail.com', 
                '7008GC@7008gc'
            )
            self.stdout.write(self.style.SUCCESS(' Superuser Jeremiah created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('ℹ Superuser Jeremiah already exists'))
