from django.test import TestCase
from django.urls import reverse


class StaticPageTests(TestCase):
    def test_privacy_policy_page_renders(self):
        response = self.client.get(reverse('privacy'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Privacy Policy')

    def test_terms_page_renders(self):
        response = self.client.get(reverse('terms'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Terms &amp; Conditions')
