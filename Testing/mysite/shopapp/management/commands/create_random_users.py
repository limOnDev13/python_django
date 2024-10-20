import random
import string

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    help = "Create random users"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of users")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random users...")

        for _ in range(count):
            User.objects.create_user(
                username="".join(random.choices(string.ascii_letters, k=random.randint(5, 20))),
                password="".join(random.choices(string.ascii_letters, k=random.randint(5, 10))),
            )
        self.stdout.write("Done")
