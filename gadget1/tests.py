import json

from django.test import TestCase
from django.urls import reverse

from .models import ContactSubmission, Order, Product


class StaticPageTests(TestCase):
    def test_privacy_policy_page_renders(self):
        response = self.client.get(reverse('privacy'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Privacy Policy')

    def test_terms_page_renders(self):
        response = self.client.get(reverse('terms'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Terms &amp; Conditions')


class ShopAndCatalogTests(TestCase):
    def test_shop_filter_can_return_all_categories(self):
        response = self.client.get(reverse('shop'), {'category': 'all'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Categories')

    def test_product_detail_page_renders(self):
        product = Product.objects.first()

        response = self.client.get(product.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)


class ContactFlowTests(TestCase):
    def test_contact_page_renders_form(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send a message')

    def test_contact_form_submission_is_saved(self):
        response = self.client.post(
            reverse('contact'),
            data={
                'name': 'Taylor Buyer',
                'email': 'taylor@example.com',
                'phone': '+263770123456',
                'topic': 'order',
                'message': 'Please confirm stock for the items in my cart.',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertContains(response, 'order request has been received')

    def test_order_request_submission_creates_order_record(self):
        product = Product.objects.first()

        response = self.client.post(
            reverse('contact'),
            data={
                'name': 'Taylor Buyer',
                'email': 'taylor@example.com',
                'phone': '+263770123456',
                'topic': 'order',
                'message': 'Please leave the package with reception if I am unavailable.',
                'order_payload': json.dumps([{'id': product.pk, 'quantity': 2}]),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactSubmission.objects.count(), 1)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.get()
        self.assertEqual(order.customer_name, 'Taylor Buyer')
        self.assertEqual(order.contact_submission.name, 'Taylor Buyer')
        self.assertEqual(order.status, Order.STATUS_PENDING)
        self.assertEqual(order.subtotal, product.price * 2)
        self.assertEqual(order.items.count(), 1)

        item = order.items.get()
        self.assertEqual(item.product, product)
        self.assertEqual(item.product_identifier, product.pk)
        self.assertEqual(item.product_name, product.name)
        self.assertEqual(item.quantity, 2)
        self.assertContains(response, f'order #{order.pk}')
