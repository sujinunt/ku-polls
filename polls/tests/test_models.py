"""Test model"""
import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Question


def create_question(question_text, days):
    """

    Create question function for tested.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    time_end = timezone.now() + datetime.timedelta(days=days+3)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time_end)


class QuestionModelTests(TestCase):
    """Test Question Model that method is work correctly."""

    def test_was_published_recently_with_future_question(self):
        """

        Test question was published recently with future question.

        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """

        Test question was published recently with old question.

        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """

        Test question was published recently with recent question.

        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_question_is_published(self):
        """

        Test question is published.

        is_published() returns True if current date is on or after
        question’s publication date.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.now() + datetime.timedelta(days=3, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.is_published(), True)

    def test_question_is_not_published(self):
        """

        Test question is not published.

        is_published() returns False if current date is after
        question’s end date.
        """
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        time_end = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.is_published(), False)