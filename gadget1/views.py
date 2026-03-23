from django.shortcuts import render
from django.db import models
from .models import Product

# Create your views here.
def index(request):
    # Get all products and bestsellers from database
    all_products = Product.objects.all()
    bestsellers = Product.objects.filter(is_bestseller=True)
    
    context = {
        'products': all_products,
        'bestsellers': bestsellers,
    }
    return render(request, 'index.html', context)

def shop_view(request):
    # Get all products from database
    products = Product.objects.all()
    
    # Get category filter from query params
    category = request.GET.get('category')
    if category and category != 'all':
        products = products.filter(category=category)
    
    # Get search term from query params
    search_term = request.GET.get('search')
    if search_term:
        products = products.filter(
            models.Q(name__icontains=search_term) | 
            models.Q(description__icontains=search_term)
        )
    
    # Get sort option from query params
    sort = request.GET.get('sort', 'default')
    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    elif sort == 'name-asc':
        products = products.order_by('name')
    elif sort == 'name-desc':
        products = products.order_by('-name')
    
    context = {
        'products': products,
    }
    return render(request, 'shop.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request,'contact.html')