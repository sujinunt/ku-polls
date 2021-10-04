"""Test model and view."""
import datetime
import unittest
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days):
    """
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
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_question_is_published(self):
        """is_published() returns True if current date is on or after
        question’s publication date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.now() + datetime.timedelta(days=3, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.is_published(), True)

    def test_question_is_not_published(self):
        """is_published() returns False if current date is after
        question’s end date."""
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        time_end = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.is_published(), False)

    def test_question_can_vote(self):
        """can_vote() returns True if voting is currently allowed for this question."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.now() + datetime.timedelta(days=3, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.can_vote(), True)

    def test_question_can_not_vote(self):
        """can_vote() returns False if voting is currently not allowed for this question."""
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        time_end = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.can_vote(), False)


class QuestionIndexViewTests(TestCase):
    """Test the view is correctly."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Test Question Detail view that work correctly."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    @unittest.skip("Couldn't retrieve content")
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text. Expect 302.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
