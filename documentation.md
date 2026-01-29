# GadgetWorld E-Commerce Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Payment Integration](#payment-integration)
   - [PayNow](#paynow)
   - [EcoCash](#ecocash)
5. [Admin Panel](#admin-panel)
6. [Customization](#customization)

---

## Project Overview

GadgetWorld is a Django-based e-commerce platform for selling electronic gadgets and tech products. Features include:
- Product catalog with categories (Smartphones, Laptops, Audio, Gaming, etc.)
- Shopping cart functionality
- Admin panel for product management
- Responsive design with dark/light theme toggle

---

## Installation

```bash
# Navigate to project directory
cd /home/brandon/Desktop/Gagdet/GadgetWorld

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Access the site at: **http://127.0.0.1:8000**
Admin panel: **http://127.0.0.1:8000/admin/**

---

## Project Structure

```
GadgetWorld/
├── gadget1/
│   ├── models.py         # Product model definition
│   ├── views.py          # Home and Shop views
│   ├── urls.py           # App URL routing
│   ├── admin.py          # Admin configuration
│   └── migrations/       # Database migrations
├── templates/
│   ├── index.html        # Homepage template
│   └── shop.html         # Shop page template
├── static/
│   ├── style.css         # Main stylesheet
│   ├── script.js         # Frontend JavaScript
│   └── products.js       # Static products data
├── GadgetWorld/
│   ├── settings.py       # Django settings
│   └── urls.py           # Root URL configuration
├── db.sqlite3            # SQLite database
└── manage.py             # Django management script
```

---

## Payment Integration

### PayNow

PayNow is a popular payment method in Zimbabwe. Integration involves mobile money USSD codes.

#### 1. Add PayNow to Models

```python
# models.py
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)  # e.g., "PayNow"
    code = models.CharField(max_length=20)  # e.g., "*180#"
    instructions = models.TextField()
    is_active = models.BooleanField(default=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
```

#### 2. Create Order Item Model

```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # Store name in case product is deleted
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total(self):
        return self.quantity * self.price
```

#### 3. PayNow Payment View

```python
# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def payment_page(request):
    """Display payment options including PayNow"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('shop')
        
        # Calculate total
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total += float(product.price) * quantity
        
        # Create pending order
        order = Order.objects.create(
            customer_name=request.POST.get('name', ''),
            customer_email=request.POST.get('email', ''),
            customer_phone=request.POST.get('phone', ''),
            total_amount=total,
            payment_method=PaymentMethod.objects.get(name='PayNow'),
            status='pending'
        )
        
        # Create order items
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                price=product.price
            )
        
        # Store order in session for verification
        request.session['pending_order_id'] = order.id
        
        return render(request, 'paynow_payment.html', {'order': order})
    
    return redirect('shop')

def verify_payment(request):
    """Verify PayNow payment via USSD callback or manual verification"""
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        phone = request.POST.get('phone')
        
        # In production, integrate with PayNow API for verification
        # For now, store the transaction for admin verification
        
        order_id = request.session.get('pending_order_id')
        if order_id:
            order = Order.objects.get(id=order_id)
            order.transaction_id = transaction_id
            order.status = 'paid'
            order.save()
            
            # Clear cart
            request.session['cart'] = {}
            del request.session['pending_order_id']
            
            return render(request, 'payment_success.html', {'order': order})
    
    return render(request, 'payment_failed.html')
```

#### 4. PayNow Payment Template

```html
<!-- templates/paynow_payment.html -->
{% extends 'base.html' %}

{% block content %}
<div class="container payment-page">
    <h2>Complete Your Payment</h2>
    
    <div class="order-summary">
        <h3>Order #{{ order.id }}</h3>
        <p>Total: <strong>${{ order.total_amount }}</strong></p>
    </div>
    
    <div class="payment-instructions">
        <h3>PayNow Instructions</h3>
        <div class="paynow-steps">
            <div class="step">
                <span class="step-number">1</span>
                <p>Dial <strong>*180#</strong> from your mobile phone</p>
            </div>
            <div class="step">
                <span class="step-number">2</span>
                <p>Select <strong>1. Make Payment</strong></p>
            </div>
            <div class="step">
                <span class="step-number">3</span>
                <p>Enter Merchant Code: <strong>GADGETWORLD</strong></p>
            </div>
            <div class="step">
                <span class="step-number">4</span>
                <p>Enter Amount: <strong>${{ order.total_amount }}</strong></p>
            </div>
            <div class="step">
                <span class="step-number">5</span>
                <p>Enter Reference: <strong>ORDER{{ order.id }}</strong></p>
            </div>
        </div>
    </div>
    
    <form method="POST" action="{% url 'verify_payment' %}" class="payment-verification-form">
        {% csrf_token %}
        <div class="form-group">
            <label for="transaction_id">Enter Transaction ID / Confirmation Number:</label>
            <input type="text" id="transaction_id" name="transaction_id" required 
                   placeholder="e.g., TXN123456">
        </div>
        <div class="form-group">
            <label for="phone">Your Phone Number:</label>
            <input type="text" id="phone" name="phone" required 
                   placeholder="e.g., 0771234567">
        </div>
        <button type="submit" class="btn btn-primary">Verify Payment</button>
    </form>
</div>
{% endblock %}
```

#### 5. PayNow URLs

```python
# urls.py
urlpatterns = [
    path('payment/paynow/', views.payment_page, name='paynow_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    # ... other paths
]
```

---

### EcoCash

EcoCash is another popular mobile money service in Zimbabwe. Integration follows a similar pattern.

#### 1. Add EcoCash to Payment Methods

```python
# models.py
# EcoCash PaymentMethod is created the same way
PaymentMethod.objects.create(
    name='EcoCash',
    code='*151#',
    instructions='Dial *151# to make payment'
)
```

#### 2. EcoCash Payment View

```python
# views.py
def ecocash_payment_page(request):
    """Display EcoCash payment instructions"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('shop')
        
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total += float(product.price) * quantity
        
        order = Order.objects.create(
            customer_name=request.POST.get('name', ''),
            customer_email=request.POST.get('email', ''),
            customer_phone=request.POST.get('phone', ''),
            total_amount=total,
            payment_method=PaymentMethod.objects.get(name='EcoCash'),
            status='pending'
        )
        
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                price=product.price
            )
        
        request.session['pending_order_id'] = order.id
        
        return render(request, 'ecocash_payment.html', {'order': order})
    
    return redirect('shop')
```

#### 3. EcoCash Payment Template

```html
<!-- templates/ecocash_payment.html -->
{% extends 'base.html' %}

{% block content %}
<div class="container payment-page">
    <h2>Complete Your Payment with EcoCash</h2>
    
    <div class="order-summary">
        <h3>Order #{{ order.id }}</h3>
        <p>Total: <strong>${{ order.total_amount }}</strong></p>
    </div>
    
    <div class="payment-instructions">
        <h3>EcoCash Instructions</h3>
        <div class="ecocash-steps">
            <div class="step">
                <span class="step-number">1</span>
                <p>Dial <strong>*151#</strong> from your mobile phone</p>
            </div>
            <div class="step">
                <span class="step-number">2</span>
                <p>Select <strong>1. EcoCash</strong></p>
            </div>
            <div class="step">
                <span class="step-number">3</span>
                <p>Select <strong>4. Make Payment</strong></p>
            </div>
            <div class="step">
                <span class="step-number">4</span>
                <p>Enter Merchant Name: <strong>GADGETWORLD</strong></p>
            </div>
            <div class="step">
                <span class="step-number">5</span>
                <p>Enter Amount: <strong>${{ order.total_amount }}</strong></p>
            </div>
            <div class="step">
                <span class="step-number">6</span>
                <p>Enter Reference: <strong>ORDER{{ order.id }}</strong></p>
            </div>
        </div>
    </div>
    
    <form method="POST" action="{% url 'verify_ecocash' %}" class="payment-verification-form">
        {% csrf_token %}
        <div class="form-group">
            <label for="transaction_id">Enter Transaction ID / Confirmation Number:</label>
            <input type="text" id="transaction_id" name="transaction_id" required 
                   placeholder="e.g., ECX123456">
        </div>
        <div class="form-group">
            <label for="phone">Your EcoCash Registered Number:</label>
            <input type="text" id="phone" name="phone" required 
                   placeholder="e.g., 0771234567">
        </div>
        <button type="submit" class="btn btn-primary">Verify Payment</button>
    </form>
</div>
{% endblock %}
```

#### 4. EcoCash URLs

```python
# urls.py
urlpatterns = [
    path('payment/ecocash/', views.ecocash_payment_page, name='ecocash_payment'),
    path('payment/verify-ecocash/', views.verify_ecocash_payment, name='verify_ecocash'),
    # ... other paths
]
```

---

## Payment Selection Page

Create a unified payment selection page:

```html
<!-- templates/payment_select.html -->
{% extends 'base.html' %}

{% block content %}
<div class="container payment-options">
    <h2>Select Payment Method</h2>
    <div class="cart-summary">
        <p>Total to Pay: <strong>${{ total }}</strong></p>
    </div>
    
    <div class="payment-methods-grid">
        <div class="payment-method-card">
            <h3>PayNow</h3>
            <p>Mobile money via *180#</p>
            <a href="{% url 'paynow_payment' %}" class="btn btn-primary">Pay with PayNow</a>
        </div>
        
        <div class="payment-method-card">
            <h3>EcoCash</h3>
            <p>Mobile money via *151#</p>
            <a href="{% url 'ecocash_payment' %}" class="btn btn-primary">Pay with EcoCash</a>
        </div>
        
        <div class="payment-method-card">
            <h3>Cash on Delivery</h3>
            <p>Pay when you receive your order</p>
            <a href="{% url 'cod_payment' %}" class="btn btn-secondary">Select COD</a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Admin Panel

### Accessing the Admin Panel

1. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Navigate to: **http://127.0.0.1:8000/admin/**

3. Log in with your superuser credentials

### Managing Products

From the admin panel, you can:
- View all products
- Add new products
- Edit existing products
- Delete products
- Mark products as bestsellers
- Filter by category

### Managing Orders

1. View all orders in the Orders section
2. See order status (pending, paid, processing, shipped, delivered)
3. Update order status
4. View order items
5. Filter orders by status

---

## Customization

### Styling

Edit `static/style.css` to customize the look and feel.

### Adding New Categories

Edit `gadget1/models.py`:

```python
CATEGORY_CHOICES = [
    ('smartphones', 'Smartphones'),
    ('laptops', 'Laptops'),
    ('tablets', 'Tablets'),
    ('audio', 'Audio'),
    ('cameras', 'Cameras'),
    ('wearables', 'Wearables'),
    ('gaming', 'Gaming'),
    ('accessories', 'Accessories'),
    # Add new category here
    ('new_category', 'New Category Name'),
]
```

### Adding New Payment Methods

1. Create a new payment template (e.g., `new_payment.html`)
2. Add a new view function
3. Add URL patterns
4. Update the payment selection page

---

## API Integration (Optional)

For production use, integrate with official APIs:

### PayNow API

```python
# Example API integration
import requests

def paynow_api_payment(mobile, amount, reference):
    api_url = "https://api.paynow.co.zw/v1/payment"
    headers = {"Authorization": f"Bearer {settings.PAYNOW_API_KEY}"}
    data = {
        "mobile": mobile,
        "amount": amount,
        "reference": reference,
        "callback_url": "https://yourdomain.com/webhook/paynow/"
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()
```

### EcoCash API

```python
# Example API integration
def ecocash_api_payment(mobile, amount, reference):
    api_url = "https://api.ecocash.co.zw/v1/payment"
    headers = {"Authorization": f"Bearer {settings.ECOCASH_API_KEY}"}
    data = {
        "subscriber_number": mobile,
        "amount": amount,
        "transaction_reference": reference
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()
```

---

## Troubleshooting

### Common Issues

1. **Products not displaying**: Ensure migrations are run and products exist in database
2. **Admin not showing Product model**: Check that `admin.site.register(Product)` is in admin.py
3. **Static files not loading**: Run `python manage.py collectstatic`
4. **Payment verification failing**: Check that transaction IDs match

### Development Tips

- Use Django Debug Toolbar for debugging
- Check Django logs in terminal for errors
- Test payment flows with test phone numbers
- Use Django's built-in testing framework

---

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Payment provider support: PayNow/EcoCash merchant support

