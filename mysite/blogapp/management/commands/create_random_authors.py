import random
import string
from typing import List

from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Author


class Command(BaseCommand):
    help = "Create random Authors."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of authors")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random authors...")

        authors: List[Author] = [
            Author(
                name="".join(random.choices(string.ascii_letters, k=random.randint(1, 20))),
                bio="".join(random.choices(string.ascii_letters, k=random.randint(1, 20))),
            )
            for _ in range(count)
        ]
        Author.objects.bulk_create(authors)

        self.stdout.write("Done")
