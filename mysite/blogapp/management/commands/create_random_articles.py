import random
import string
from typing import List

from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Count

from blogapp.models import Article, Category, Author, Tag


class Command(BaseCommand):
    help = "Create random articles. Each article requires a author, a category and tags, "\
           "so first add authors (for example, with the create_random_authors command), "\
           "add tags (for example, with the create_random_tags command) and "\
           "add categories (for example, with the create_random_categories command)"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Count of articles")

    @transaction.atomic
    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        self.stdout.write(f"Creating {count} random articles...")

        authors: List[Author] = Author.objects.all()
        categories: List[Category] = Category.objects.all()
        tags: List[Tag] = Tag.objects.all()
        count_tags: int = Tag.objects.aggregate(count=Count("pk"))["count"]

        articles: List[Article] = [
            Article(
                title="".join(random.choices(string.ascii_letters, k=random.randint(1, 200))),
                content="".join(random.choices(string.ascii_letters, k=random.randint(1, 200))),
                author=random.choice(authors),
                category=random.choice(categories),
            )
            for _ in range(random.randint(0, count))
        ]
        Article.objects.bulk_create(articles)

        for article in articles:
            article.tags.set(
                random.choices(
                    tags,
                    k=random.randint(0, count_tags)
                )
            )

        self.stdout.write("Done")
