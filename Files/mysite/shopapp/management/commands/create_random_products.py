import random
import string

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    help = ("Create random products. Each product requires a user,"
            " so first add users (for example, with the create_random_users command)")

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of products")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random products...")

        for _ in range(count):
            Product.objects.create(
                name="".join(random.choices(string.ascii_letters, k=random.randint(5, 99))),
                description="".join(random.choices(string.ascii_letters, k=random.randint(5, 99))),
                price=round(random.uniform(0, 100), 2),
                discount=round(random.uniform(0, 100), 2),
                created_by=random.choice(User.objects.all()),
                archived=random.choice((True, False)),
            )
        self.stdout.write("Done")
