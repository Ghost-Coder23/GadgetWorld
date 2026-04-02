from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('smartphones', 'Smartphones'),
        ('laptops', 'Laptops'),
        ('accessories', 'Accessories'),
        ('grocery','Groceries'),
        ('footwear','Footwear'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    imageSrc = models.URLField(max_length=500, blank=True, default='')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_bestseller = models.BooleanField(default=False)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return self.imageSrc
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

class Promotion(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="Enter features as bullet points, one per line")
    button_text = models.CharField(max_length=100, default="View Deals", blank=True)
    button_link = models.URLField(max_length=500, default="/shop/", blank=True)
    active = models.BooleanField(default=True, help_text="Show on home page?")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name_plural = "Promotions"

    def __str__(self):
        return self.title
    
    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []
