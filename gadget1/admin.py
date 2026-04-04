from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import ContactSubmission, Order, OrderItem, Product, Promotion

admin.site.site_header = 'Curated Admin'
admin.site.site_title = 'Curated Control Room'
admin.site.index_title = 'Inventory, orders, and customer operations'

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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ['product_name', 'product_identifier', 'quantity', 'unit_price', 'line_total_display', 'linked_product']
    readonly_fields = fields

    @admin.display(description='Line total')
    def line_total_display(self, obj):
        return f'${obj.line_total:.2f}'

    @admin.display(description='Product')
    def linked_product(self, obj):
        if not obj.product_id:
            return 'Product removed from catalog'

        product_url = reverse('admin:gadget1_product_change', args=[obj.product_id])
        return format_html('<a href="{}">Open product</a>', product_url)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'status', 'subtotal', 'item_count_display', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'customer_name', 'email', 'phone', 'notes', 'items__product_name', 'items__product_identifier']
    ordering = ['-created_at']
    list_editable = ['status']
    readonly_fields = ['subtotal', 'item_count_display', 'linked_submission', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer', {
            'fields': ('customer_name', 'email', 'phone')
        }),
        ('Order Status', {
            'fields': ('status', 'subtotal', 'item_count_display')
        }),
        ('Notes & Source', {
            'fields': ('notes', 'linked_submission')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

    @admin.display(description='Items')
    def item_count_display(self, obj):
        return obj.item_count

    @admin.display(description='Contact submission')
    def linked_submission(self, obj):
        if not obj.contact_submission_id:
            return 'Not linked'

        submission_url = reverse('admin:gadget1_contactsubmission_change', args=[obj.contact_submission_id])
        return format_html('<a href="{}">View original request</a>', submission_url)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'topic', 'created_at', 'linked_order']
    list_filter = ['topic', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'linked_order']

    @admin.display(description='Order')
    def linked_order(self, obj):
        try:
            order = obj.order
        except Order.DoesNotExist:
            return 'No order'

        order_url = reverse('admin:gadget1_order_change', args=[order.pk])
        return format_html('<a href="{}">Open order #{}</a>', order_url, order.pk)
