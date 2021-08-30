import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    '''The polls question with question text and date published'''
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        '''String of the question text'''
        return self.question_text

    def was_published_recently(self):
        '''Return True if the question is published in the last 1 day'''
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    '''The polls answer choice of the polls question'''
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        '''String of choice text'''
        return self.choice_text
