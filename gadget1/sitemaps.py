from django.contrib.sitemaps import Sitemap
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return None
    
    def location(self, obj):
        return '/shop/'  # All products on shop page


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['home', 'shop', 'about', 'contact', 'privacy', 'terms']
    
    def location(self, view_name):
        if view_name == 'home':
            return '/'
        elif view_name == 'shop':
            return '/shop/'
        elif view_name == 'about':
            return '/about/'
        elif view_name == 'contact':
            return '/contact/'
        elif view_name == 'privacy':
            return '/privacy-policy/'
        elif view_name == 'terms':
            return '/terms-and-conditions/'
