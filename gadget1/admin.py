from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Product, Promotion

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'is_bestseller', 'image_preview', 'edit_product']
    list_filter = ['category', 'is_bestseller']
    search_fields = ['name', 'description']
    ordering = ['id',]
    
    # Group fields in sections
    fieldsets = (
        ('Product Information', {
            'fields': ('id', 'name', 'category', 'price', 'unit')
        }),
        ('Details', {
            'fields': ('description', 'image', 'imageSrc', 'image_preview'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Status', {
            'fields': ('is_bestseller',),
        }),
    )
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" alt="{}" style="max-height: 72px; border-radius: 8px;" />',
                obj.image_url,
                obj.name,
            )
        return "No image"

    image_preview.short_description = "Preview"

    def edit_product(self, obj):
        edit_url = reverse('admin:gadget1_product_change', args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', edit_url)

    edit_product.short_description = "Edit Product"
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
