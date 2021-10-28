import django.test
import datetime
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

class VoteTests(django.test.TestCase):
    """Test for user vote."""

    def test_can_vote(self):
        """can_vote() returns True if voting is currently allowed for this question."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.now() + datetime.timedelta(days=3, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.can_vote(), True)

    def test_can_not_vote(self):
        """can_vote() returns False if voting is currently not allowed for this question."""
        time = timezone.now() - datetime.timedelta(days=3, seconds=1)
        time_end = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pub_question = Question(pub_date=time, end_date=time_end)
        self.assertIs(pub_question.can_vote(), False)