from django.shortcuts import render
from django.views.generic import ListView

from .models import Article


# Create your views here.
class ArticlesListView(ListView):
    queryset = (Article.objects.defer("content")
                .select_related("author").defer("author__bio")
                .select_related("category")
                .prefetch_related("tags"))
