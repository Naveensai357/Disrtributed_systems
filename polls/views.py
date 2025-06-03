from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote(request.user):
        messages.error(request, "You have already voted on this poll!")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        if not question.can_vote(request.user):
            messages.error(request, "You have already voted on this poll!")
            return redirect('polls:index')
            
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        question.voters.add(request.user)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@user_passes_test(is_admin)
def resultsData(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    votes = []
    for choice in question.choice_set.all():
        votes.append({choice.choice_text: choice.votes})
    return JsonResponse(votes, safe=False)