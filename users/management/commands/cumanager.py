from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание пользователя maneger'

    def handle(self, *args, **options):
        user = User.objects.create(
            email='maneger1@sky.pro',
            first_name='maneger',
            last_name='maneger',
            is_staff=True,
            is_superuser=False,
        )

        user.set_password('123s')
        user.save()



