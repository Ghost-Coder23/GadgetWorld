from django.test import TestCase
from django.urls import reverse

from .models import ContactSubmission, Product


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
