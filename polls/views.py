from django.http import HttpResponse, Http404
#from django.template import loader
from django.shortcuts import render
from .models import Question

def index(request):
    '''Polls index page that show lastest 5 question'''
    lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {"latest_question_list": lastest_question_list,}
    #return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    '''Show question detail to User'''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    '''Show question results to User'''
    return HttpResponse(f"You're looking at the results of question {question_id}.")

def vote(request, question_id):
    '''Show user vote to User'''
    return HttpResponse(f"You are voting question {question_id}.")
