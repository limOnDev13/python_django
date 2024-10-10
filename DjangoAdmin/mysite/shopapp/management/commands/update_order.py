from typing import List

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order, Product


class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **options):
        self.stdout.write("Update order")

        order = Order.objects.first()
        if not order:
            self.stdout.write("Order not exists")
            return

        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()

        self.stdout.write("Done")
