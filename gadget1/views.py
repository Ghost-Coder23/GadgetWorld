import json
from decimal import Decimal

from django.contrib import messages
from django.db import models, transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactSubmissionForm
from .models import ContactSubmission, Order, OrderItem, Product, Promotion


HOME_CATEGORY_ORDER = ['smartphones', 'laptops', 'audio', 'gaming', 'wearables', 'accessories']
SORT_OPTIONS = {'default', 'price-asc', 'price-desc', 'name-asc', 'name-desc'}
MAX_ORDER_ITEM_QUANTITY = 50
DEFAULT_ORDER_MESSAGE = 'Please confirm availability, delivery options, and payment details for the items listed above.'


def build_category_choices():
    label_map = dict(Product.CATEGORY_CHOICES)
    categories = sorted(
        set(Product.objects.values_list('category', flat=True)),
        key=lambda value: (
            next((index for index, (choice, _) in enumerate(Product.CATEGORY_CHOICES) if choice == value), len(Product.CATEGORY_CHOICES)),
            value,
        ),
    )
    return [{'value': category, 'label': label_map.get(category, category.replace('-', ' ').title())} for category in categories]


def build_home_categories():
    products_by_category = {}
    for product in Product.objects.filter(category__in=HOME_CATEGORY_ORDER).order_by('category', 'id'):
        products_by_category.setdefault(product.category, product)

    label_map = dict(Product.CATEGORY_CHOICES)
    return [
        {
            'slug': category,
            'label': label_map.get(category, category.replace('-', ' ').title()),
            'image_url': products_by_category[category].image_url,
        }
        for category in HOME_CATEGORY_ORDER
        if category in products_by_category
    ]


def apply_shop_filters(queryset, *, category='all', search_term='', sort='default'):
    filtered = queryset

    if category and category != 'all':
        filtered = filtered.filter(category=category)

    if search_term:
        filtered = filtered.filter(
            models.Q(name__icontains=search_term) |
            models.Q(description__icontains=search_term)
        )

    if sort == 'price-asc':
        filtered = filtered.order_by('price')
    elif sort == 'price-desc':
        filtered = filtered.order_by('-price')
    elif sort == 'name-asc':
        filtered = filtered.order_by('name')
    elif sort == 'name-desc':
        filtered = filtered.order_by('-name')

    return filtered


def normalize_order_payload(raw_payload):
    if not raw_payload:
        return []

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        return []

    if not isinstance(payload, list):
        return []

    product_quantities = {}
    product_order = []

    for item in payload:
        if not isinstance(item, dict):
            continue

        product_id = str(item.get('id', '')).strip()
        if not product_id:
            continue

        try:
            quantity = int(item.get('quantity', 1))
        except (TypeError, ValueError):
            continue

        quantity = max(1, min(quantity, MAX_ORDER_ITEM_QUANTITY))
        if product_id not in product_quantities:
            product_quantities[product_id] = 0
            product_order.append(product_id)

        product_quantities[product_id] = min(MAX_ORDER_ITEM_QUANTITY, product_quantities[product_id] + quantity)

    return [(product_id, product_quantities[product_id]) for product_id in product_order]


def build_order_request(raw_payload):
    normalized_items = normalize_order_payload(raw_payload)
    if not normalized_items:
        return None

    product_ids = [product_id for product_id, _ in normalized_items]
    products_by_id = Product.objects.in_bulk(product_ids)

    items = []
    subtotal = Decimal('0.00')

    for product_id, quantity in normalized_items:
        product = products_by_id.get(product_id)
        if not product:
            continue

        line_total = product.price * quantity
        subtotal += line_total
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'line_total': line_total,
            }
        )

    if not items:
        return None

    payload = json.dumps(
        [{'id': item['product'].pk, 'quantity': item['quantity']} for item in items],
        separators=(',', ':'),
    )

    return {
        'items': items,
        'subtotal': subtotal,
        'payload': payload,
    }


def contact_form_initial(request, *, order_request=None):
    initial = {}
    valid_topics = {choice[0] for choice in ContactSubmission.TOPIC_CHOICES}

    topic = request.GET.get('topic', '').strip()
    if topic in valid_topics:
        initial['topic'] = topic

    message = request.GET.get('message', '').strip()
    if order_request:
        initial['topic'] = 'order'
        initial['order_payload'] = order_request['payload']
        initial['message'] = message or DEFAULT_ORDER_MESSAGE
    elif message:
        initial['message'] = message

    return initial


def create_order_from_submission(submission, order_request):
    order = Order.objects.create(
        contact_submission=submission,
        customer_name=submission.name,
        email=submission.email,
        phone=submission.phone,
        status=Order.STATUS_PENDING,
        notes=submission.message.strip(),
        subtotal=order_request['subtotal'],
    )
    OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                product=item['product'],
                product_identifier=item['product'].pk,
                product_name=item['product'].name,
                unit=item['product'].unit,
                unit_price=item['product'].price,
                quantity=item['quantity'],
            )
            for item in order_request['items']
        ]
    )
    return order


def apply_order_form_state(form, order_request):
    if order_request:
        form.fields['message'].widget.attrs['placeholder'] = 'Add delivery notes, preferred timing, or any special instructions.'

# Create your views here.
def index(request):
    # Get all products and bestsellers from database
    all_products = Product.objects.all()
    bestsellers = Product.objects.filter(is_bestseller=True)
    promotion = Promotion.objects.filter(active=True).order_by('order').first()
    
    context = {
        'products': all_products,
        'bestsellers': bestsellers,
        'bestseller_ids': list(bestsellers.values_list('id', flat=True)),
        'featured_categories': build_home_categories(),
        'promotion': promotion,
    }
    return render(request, 'index.html', context)

def shop_view(request):
    products = Product.objects.all()
    available_categories = build_category_choices()
    valid_categories = {category['value'] for category in available_categories}

    selected_category = request.GET.get('category', 'all').strip() or 'all'
    if selected_category != 'all' and selected_category not in valid_categories:
        selected_category = 'all'

    search_term = request.GET.get('search', '').strip()
    selected_sort = request.GET.get('sort', 'default').strip()
    if selected_sort not in SORT_OPTIONS:
        selected_sort = 'default'

    filtered_products = apply_shop_filters(
        products,
        category=selected_category,
        search_term=search_term,
        sort=selected_sort,
    )

    context = {
        'products': filtered_products,
        'available_categories': available_categories,
        'selected_category': selected_category,
        'selected_sort': selected_sort,
        'search_term': search_term,
    }
    return render(request, 'shop.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        raw_order_payload = request.POST.get('order_payload', '').strip()
        order_request = build_order_request(raw_order_payload)
        form = ContactSubmissionForm(request.POST)
        apply_order_form_state(form, order_request)
        if form.is_valid():
            wants_checkout_order = form.cleaned_data['topic'] == 'order' and bool(raw_order_payload)
            if wants_checkout_order and not order_request:
                form.add_error(None, 'We could not verify the items in your order. Please return to your cart and try again.')
            else:
                with transaction.atomic():
                    submission = form.save()
                    order = create_order_from_submission(submission, order_request) if wants_checkout_order else None

                if order is not None:
                    messages.success(
                        request,
                        f'Your order request has been received as order #{order.pk}. We will contact you to confirm availability and next steps.',
                    )
                else:
                    messages.success(
                        request,
                        'Your message has been sent. We will get back to you shortly.'
                        if submission.topic != 'order'
                        else 'Your order request has been received. We will contact you to confirm availability and next steps.',
                    )
                return redirect('contact')
    else:
        order_request = build_order_request(request.GET.get('cart', '').strip())
        initial = contact_form_initial(request, order_request=order_request)
        form = ContactSubmissionForm(initial=initial)
        apply_order_form_state(form, order_request)

    prefilled_from_cart = bool(order_request)

    return render(
        request,
        'contact.html',
        {
            'form': form,
            'prefilled_from_cart': prefilled_from_cart,
            'prefilled_order_items': order_request['items'] if order_request else [],
            'prefilled_order_subtotal': order_request['subtotal'] if order_request else None,
        },
    )

def privacy_policy(request):
    return render(request, 'privacy.html')

def terms_and_conditions(request):
    return render(request, 'terms.html')
