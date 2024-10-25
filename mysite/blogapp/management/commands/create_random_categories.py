import random
import string
from typing import List

from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Category


class Command(BaseCommand):
    help = "Create random categories."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of categories")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random categories...")

        categories: List[Category] = [
            Category(name="".join(random.choices(string.ascii_letters, k=random.randint(1, 40))))
            for _ in range(count)
        ]
        Category.objects.bulk_create(categories)

        self.stdout.write("Done")
