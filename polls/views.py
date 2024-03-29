"""View of Django web."""
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """Polls index page that show lastest 5 question."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions but not including those set to be published in the future."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Show question detail to User."""

    model = Question
    template_name = 'polls/detail.html'


def detail(request, pk):
    """Show question detail to user."""
    question = get_object_or_404(Question, pk=pk)
    if question.pub_date > timezone.now():
        messages.error(request, f"{'The question is not available for vote'}")
        return redirect("polls:index")
    elif timezone.now() >= question.end_date:
        messages.error(request, f"{'The question vote is ended'}")
        return redirect("polls:index")
    else:
        context = {'question': question}
        return render(request, 'polls/detail.html', context)


class ResultsView(generic.DetailView):
    """Show question results to User."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Show user vote."""
    user = request.user
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select choice answer."
        })
    else:
        Vote.objects.update_or_create(user=user, question=question, defaults={'selected_choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(selected_choice=choice).count()
            choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
