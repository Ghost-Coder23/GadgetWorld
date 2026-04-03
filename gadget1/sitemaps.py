from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return None
    
    def location(self, obj):
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['home', 'shop', 'about', 'contact', 'privacy', 'terms']
    
    def location(self, view_name):
        return reverse(view_name)
