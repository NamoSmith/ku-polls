"""Programs for the view of polls."""
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Index View Class."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions
        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail View Class."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Result View class."""

    model = Question
    template_name = 'polls/result.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """If there is no vote, redirect users to the page before and print an error message."""

    user = request.user
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        logger.info(f'{user} voted on {question}')
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if user.vote_set.filter(user=user).exists():
            vote = user.vote_set.get(user=user)
            vote.choice = selected_choice
            vote.save()
        else:
            Vote.objects.create(user=user, choice=selected_choice)
        logger.info(f"User {user.username} submit a vote for question {question.id} ")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def show_detail(request, pk):
    """Question detail page show the questions and choices for voting."""

    question = get_object_or_404(Question, pk=pk)
    if not question.can_vote():
        messages.error(
            request,
            f'Error: poll "{question.question_text}" is no longer publish.'
        )
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/detail.html', {'question': question})


logger = logging.getLogger("polls")


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def login_logging(sender, request, user, **kwargs):
    """Show a logging info after the user is logged in."""

    logger.info(f"User: {user.username} logged in from {get_client_ip(request)}")


@receiver(user_logged_out)
def logout_logging(sender, request, user, **kwargs):
    """Show a logging info after the user is logged out."""

    logger.info(f"User: {user.username} logged out from {get_client_ip(request)}")


@receiver(user_login_failed)
def failed_login_logging(sender, request, credentials, **kwargs):
    """Show a warning logging info after the user enters wrong username or password."""

    logger.warning(f"Invalid login attempt for User: {credentials['username']} from {get_client_ip(request)}")
