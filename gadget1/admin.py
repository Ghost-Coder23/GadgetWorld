from django.contrib import admin
from .models import Product, Promotion

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'is_bestseller']
    list_filter = ['category', 'is_bestseller']
    search_fields = ['name', 'description']
    ordering = ['id',]
    
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
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'order', 'created_at']
    list_filter = ['active']
    search_fields = ['title', 'description']
    ordering = ['order']
    list_editable = ['active', 'order']
    
    fieldsets = (
        ('Promotion Content', {
            'fields': ('title', 'description', 'features')
        }),
        ('Call to Action', {
            'fields': ('button_text', 'button_link'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('active', 'order'),
        }),
    )
    readonly_fields = ('created_at',)
