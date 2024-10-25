from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    bio = models.TextField()


class Category(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=True, default='')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
