from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order, Product


class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **options):
        self.stdout.write("Create order")

        user = User.objects.get(username="admin")
        order, created = Order.objects.get_or_create(
            address="address",
            user=user,
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Order created"))
        else:
            self.stdout.write("Order exists")

        self.stdout.write("Done")
