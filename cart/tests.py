from django.test import TestCase, Client
from django.urls import reverse


class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_checkout_flow_creates_order_and_clears_cart(self):
        # Simulate adding to cart via session
        session = self.client.session
        session['cart'] = {'1': 2}
        session.save()

        response = self.client.get(reverse('cart:checkout'))
        self.assertEqual(response.status_code, 200)
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'address': '123 Test Ave',
            'city': 'Testville',
            'postal_code': '12345',
            'country': 'Testland',
            'phone': '555-0123',
        }
        response = self.client.post(reverse('cart:checkout'), data)
        # Should redirect to order summary
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('orders:summary'), response['Location'])
        # After posting, last_order should be in session and cart cleared
        session = self.client.session
        self.assertIn('last_order', session)
        self.assertEqual(session.get('cart', {}), {})

    def test_remove_item_from_cart(self):
        session = self.client.session
        session['cart'] = {'2': 1, '3': 2}
        session.save()
        response = self.client.post(reverse('cart:remove', args=[2]))
        # After removal, redirect back to cart
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertNotIn('2', session.get('cart', {}))
        # Ensure other items remain
        self.assertIn('3', session.get('cart', {}))
