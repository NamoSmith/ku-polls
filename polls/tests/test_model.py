"""Tests for Model."""

import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the given
    number of `days` offset to now (negative for questions published in the past,
    positive for questions that have yet to be published).
    Args:
        question_text
        days
    Returns: Question object
    """

    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Tests for model."""

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False
        for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True
        for questions whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_old_question(self):
        """Returns True for questions that are older than the current time."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """Returns False for questions that pub_date is not arrived."""
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_in_voting_period_question(self):
        """Returns True for questions that are in voting period."""
        pub_date = timezone.now() - datetime.timedelta(days=10)
        end_date = timezone.now() + datetime.timedelta(days=10)
        published_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(published_question.can_vote(), True)

    def test_can_vote_with_before_published_question(self):
        """Returns False for questions that are not published yet."""
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=10)
        ended_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(ended_question.can_vote(), False)

    def test_can_vote_with_after_end_date_question(self):
        """Returns False for questions that their current time pass the end date."""
        pub_date = timezone.now() - datetime.timedelta(days=10)
        end_date = timezone.now() - datetime.timedelta(days=1)
        ended_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(ended_question.can_vote(), False)
