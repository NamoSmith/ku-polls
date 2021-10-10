"""This is a program for polls model."""

import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Class for a question model."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date', null=True, default=timezone.now)

    def __str__(self):
        """Return questions."""
        return self.question_text

    def was_published_recently(self):
        """Return true if question published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return true if question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return true if question are in the time that it can be voted."""
        now = timezone.now()
        return self.is_published() and now <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Class for a choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
