from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('smartphones', 'Smartphones'),
        ('laptops', 'Laptops'),
        ('tablets', 'Tablets'),
        ('audio', 'Audio'),
        ('cameras', 'Cameras'),
        ('wearables', 'Wearables'),
        ('gaming', 'Gaming'),
        ('accessories', 'Accessories'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    imageSrc = models.URLField(max_length=500)
    is_bestseller = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

