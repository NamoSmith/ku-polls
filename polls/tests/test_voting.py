"""Tests for voting with authentication system"""

import datetime
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class VotingTest(TestCase):
    """Tests for voting with different types of users."""

    def setUp(self):
        """Setup an accounts, questions, and choices"""

        self.question = Question.objects.create(
            question_text='Test question',
            pub_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=5)
        )
        for i in range(3):
            self.question.choice_set.create(choice_text=f'Choice {i}')
        self.user = {
            'username': 'test01',
            'password': 'hello123'
        }
        User.objects.create_user(**self.user)
        self.client.post(reverse('login'), self.user)

    def test_vote_for_unauthenticated_user(self):
        """Tests that unauthenticated users cannot vote and get a 302 status code after vote."""

        self.client.post(reverse('logout'))
        response = self.client.get(reverse('polls:index'))
        self.assertFalse(response.context['user'].is_active)
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': 2})
        self.assertEqual(response.status_code, 302)

    def test_vote_for_authenticated_user(self):
        """Tests that authenticated user can vote"""

        response = self.client.get(reverse('polls:index'))
        self.assertTrue(response.context['user'].is_active)
        self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': 2})
        self.assertTrue(self.question.vote_set.filter(question=self.question).exists)
