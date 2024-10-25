import random
import string
from typing import List

from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Tag


class Command(BaseCommand):
    help = "Create random tags."

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of tags")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random tags...")

        tags: List[Tag] = [
            Tag(name="".join(random.choices(string.ascii_letters, k=random.randint(1, 20))))
            for _ in range(count)
        ]
        Tag.objects.bulk_create(tags)

        self.stdout.write("Done")
