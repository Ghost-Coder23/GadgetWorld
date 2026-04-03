from django.contrib import messages
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactSubmissionForm
from .models import ContactSubmission, Product, Promotion


HOME_CATEGORY_ORDER = ['smartphones', 'laptops', 'audio', 'gaming', 'wearables', 'accessories']
SORT_OPTIONS = {'default', 'price-asc', 'price-desc', 'name-asc', 'name-desc'}


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


def contact_form_initial(request):
    initial = {}
    valid_topics = {choice[0] for choice in ContactSubmission.TOPIC_CHOICES}

    topic = request.GET.get('topic', '').strip()
    if topic in valid_topics:
        initial['topic'] = topic

    message = request.GET.get('message', '').strip()
    if message:
        initial['message'] = message

    return initial

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
    initial = contact_form_initial(request)
    prefilled_from_cart = initial.get('topic') == 'order' and bool(initial.get('message'))

    if request.method == 'POST':
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            messages.success(
                request,
                'Your message has been sent. We will get back to you shortly.'
                if submission.topic != 'order'
                else 'Your order request has been received. We will contact you to confirm availability and next steps.',
            )
            return redirect('contact')
    else:
        form = ContactSubmissionForm(initial=initial)

    return render(
        request,
        'contact.html',
        {
            'form': form,
            'prefilled_from_cart': prefilled_from_cart,
        },
    )

def privacy_policy(request):
    return render(request, 'privacy.html')

def terms_and_conditions(request):
    return render(request, 'terms.html')
