from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class BruteForceProtectionTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="securepassword123"
        )
        self.login_url = reverse('login')

    def test_brute_force_protection(self):
        # Simulate multiple failed login attempts
        for attempt in range(10):
            response = self.client.post(self.login_url, {
                'email': self.user.email,
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, 401)

        # Check if the account is locked or further attempts are blocked
        response = self.client.post(self.login_url, {
            'email': self.user.email,
            'password': 'securepassword123'
        })
        self.assertNotEqual(response.status_code, 200)
