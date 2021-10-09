"""Question and Choice Models."""
import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """The polls question with question text and date published."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        """Return string of the question text."""
        return self.question_text

    def was_published_recently(self):
        """Return True if the question is published in the last 1 day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return True if current date is on or after question's publication date."""
        now = timezone.now()
        return self.pub_date <= now < self.end_date

    def can_vote(self):
        """Return True if voting is currently allowed for this question."""
        now = timezone.now()
        return self.pub_date <= now < self.end_date


class Choice(models.Model):
    """The polls answer choice of the polls question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return string of choice text."""
        return self.choice_text
