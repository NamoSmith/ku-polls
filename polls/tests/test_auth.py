"""Tests for users authentication system."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse


class AuthTests(TestCase):
    """Simple authentication tests."""

    def setUp(self):
        """Setup an account."""

        self.user = {
            'username': 'test01',
            'password': 'hello123'
        }
        User.objects.create_user(**self.user)

    def test_login(self):
        """Test that users who logged in is authenticated."""

        response = self.client.post(reverse('login'), self.user)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        """Test that users who logged out is unauthenticated."""

        self.client.post(reverse('login'), self.user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('polls:index'))
        self.assertFalse(response.context['user'].is_authenticated)
