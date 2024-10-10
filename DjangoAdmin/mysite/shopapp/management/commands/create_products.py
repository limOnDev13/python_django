from typing import List

from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates some products
    """
    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_names: List[str] = [
            f"product_{num}"
            for num in range(1, 4)
        ]

        for name in products_names:
            product, created = Product.objects.get_or_create(
                name=name
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product {name}"))
            else:
                self.stdout.write(f"Product {name} exists")
        self.stdout.write("Done")
