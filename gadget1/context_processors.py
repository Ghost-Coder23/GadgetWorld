from .models import Product


def site_catalog(request):
    if request.path.startswith('/admin/'):
        return {'catalog_products_payload': []}

    products = Product.objects.all()
    payload = [
        {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'categoryLabel': product.category_label,
            'price': float(product.price),
            'unit': product.unit,
            'description': product.description,
            'imageSrc': product.image_url,
            'detailUrl': product.get_absolute_url(),
        }
        for product in products
    ]
    return {'catalog_products_payload': payload}
