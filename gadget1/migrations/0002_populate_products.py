from django.db import migrations

def populate_products(apps, schema_editor):
    Product = apps.get_model('gadget1', 'Product')
    products_data = [
        {
            'id': 'prod001',
            'name': 'iPhone 15 Pro Max',
            'category': 'smartphones',
            'price': '1199.00',
            'unit': '',
            'description': 'The most advanced iPhone ever with A17 Pro chip, titanium design, and powerful camera system.',
            'imageSrc': 'https://images.pexels.com/photos/129208/pexels-photo-129208.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': True,
        },
        {
            'id': 'prod002',
            'name': 'Samsung Galaxy S24 Ultra',
            'category': 'smartphones',
            'price': '1299.00',
            'unit': '',
            'description': 'Galaxy AI powered smartphone with built S Pen, 200MP camera, and titanium frame.',
            'imageSrc': 'https://images.pexels.com/photos/1618412/pexels-photo-1618412.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod003',
            'name': 'MacBook Pro 14" M3',
            'category': 'laptops',
            'price': '1999.00',
            'unit': '',
            'description': 'Power through your workflow with M3 chip, stunning Liquid Retina XDR display.',
            'imageSrc': 'https://images.pexels.com/photos/1181243/pexels-photo-1181243.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': True,
        },
        {
            'id': 'prod004',
            'name': 'Dell XPS 15 Laptop',
            'category': 'laptops',
            'price': '1499.00',
            'unit': '',
            'description': 'Premium Windows laptop with InfinityEdge display and powerful Intel Core processor.',
            'imageSrc': 'https://images.pexels.com/photos/7974/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod005',
            'name': 'iPad Pro 12.9" M2',
            'category': 'tablets',
            'price': '1099.00',
            'unit': '',
            'description': 'Supercharged by M2 chip, perfect for creativity and productivity on the go.',
            'imageSrc': 'https://images.pexels.com/photos/1334414/pexels-photo-1334414.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': True,
        },
        {
            'id': 'prod006',
            'name': 'Sony WH-1000XM5 Headphones',
            'category': 'audio',
            'price': '399.00',
            'unit': '',
            'description': 'Industry-leading noise cancellation with exceptional sound quality and 30hr battery.',
            'imageSrc': 'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': True,
        },
        {
            'id': 'prod007',
            'name': 'AirPods Pro 2nd Gen',
            'category': 'audio',
            'price': '249.00',
            'unit': '',
            'description': 'Active noise cancellation, spatial audio, and adaptive transparency.',
            'imageSrc': 'https://images.pexels.com/photos/6579238/pexels-photo-6579238.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod008',
            'name': 'Canon EOS R6 Mark II',
            'category': 'cameras',
            'price': '2499.00',
            'unit': '',
            'description': 'Full-frame mirrorless camera with 24.2MP sensor and advanced autofocus.',
            'imageSrc': 'https://images.pexels.com/photos/3850255/pexels-photo-3850255.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod009',
            'name': 'Apple Watch Series 9',
            'category': 'wearables',
            'price': '399.00',
            'unit': '',
            'description': 'Smarter, brighter, more powerful with Double Tap and S9 SiP.',
            'imageSrc': 'https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod010',
            'name': 'Samsung Galaxy Watch 6',
            'category': 'wearables',
            'price': '299.00',
            'unit': '',
            'description': 'Advanced sleep coaching and body composition with sleek design.',
            'imageSrc': 'https://images.pexels.com/photos/2540626/pexels-photo-2540626.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod011',
            'name': 'PlayStation 5 Pro',
            'category': 'gaming',
            'price': '699.00',
            'unit': '',
            'description': 'The most powerful PlayStation console with enhanced graphics and 2TB storage.',
            'imageSrc': 'https://images.pexels.com/photos/3165335/pexels-photo-3165335.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': True,
        },
        {
            'id': 'prod012',
            'name': 'Nintendo Switch OLED',
            'category': 'gaming',
            'price': '349.00',
            'unit': '',
            'description': 'Vibrant 7-inch OLED screen, wide adjustable stand, and enhanced audio.',
            'imageSrc': 'https://images.pexels.com/photos/163443/pexels-photo-163443.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod013',
            'name': 'Anker PowerBank 20000mAh',
            'category': 'accessories',
            'price': '49.99',
            'unit': '',
            'description': 'High-capacity portable charger with fast charging for all your devices.',
            'imageSrc': 'https://images.pexels.com/photos/4433837/pexels-photo-4433837.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod014',
            'name': 'Logitech MX Master 3S Mouse',
            'category': 'accessories',
            'price': '99.99',
            'unit': '',
            'description': 'Ultimate productivity mouse with electromagnetic scroll and quiet clicks.',
            'imageSrc': 'https://images.pexels.com/photos/2114369/pexels-photo-2114369.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
        {
            'id': 'prod015',
            'name': 'Samsung 49" Odyssey G9',
            'category': 'accessories',
            'price': '1499.00',
            'unit': '',
            'description': 'Ultra-wide DQHD gaming monitor with 240Hz refresh rate and 1ms response.',
            'imageSrc': 'https://images.pexels.com/photos/1029757/pexels-photo-1029757.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
            'is_bestseller': False,
        },
    ]
    
    for product_data in products_data:
        Product.objects.create(**product_data)


def reverse_products(apps, schema_editor):
    Product = apps.get_model('gadget1', 'Product')
    Product.objects.filter(id__startswith='prod').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('gadget1', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_products, reverse_products),
    ]

