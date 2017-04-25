from django.contrib.sitemaps import Sitemap
from catalog.models import Product
from catalog.settings import GROUP_PRODUCTS_BY_PARENT
from _datetime import datetime


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        if GROUP_PRODUCTS_BY_PARENT:
            return Product.objects.with_variants()
        else:
            return Product.objects.all()

    def lastmod(self, obj):
        return datetime.now()
