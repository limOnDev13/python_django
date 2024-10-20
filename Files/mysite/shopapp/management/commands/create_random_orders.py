import random
import string
from typing import List

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    help = ("Create random orders. Each order requires a user and a product,"
            " so first add users (for example, with the create_random_users command)"
            " and add products (for example, with the create_random_products command)")

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of orders")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random orders...")

        for _ in range(count):
            order: Order = Order.objects.create(
                delivery_address="".join(random.choices(string.ascii_letters, k=random.randint(5, 99))),
                promocode="".join(random.choices(string.ascii_letters, k=random.randint(5, 20))),
                user=random.choice(User.objects.all())
            )
            order.products.set(random.choices(
                Product.objects.all(),
                k=random.randint(0, Product.objects.count())),
            )
            order.save()

        self.stdout.write("Done")
