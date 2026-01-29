from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'is_bestseller')
    list_filter = ('category', 'is_bestseller')
    search_fields = ('name', 'description')
    ordering = ('id',)
    
    # Group fields in sections
    fieldsets = (
        ('Product Information', {
            'fields': ('id', 'name', 'category', 'price', 'unit')
        }),
        ('Details', {
            'fields': ('description', 'imageSrc'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Status', {
            'fields': ('is_bestseller',),
        }),
    )
