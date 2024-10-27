from django.contrib.sitemaps import Sitemap

from .models import Product


class ShopSitemap(Sitemap):
    changefreq = "always",
    priority = "0.314"

    def items(self):
        return Product.objects.order_by("price")

    def lastmod(self, obj: Product):
        return obj.created_at

