from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse

from ..models import Question, Answer
from core.decorators import ajax_required
from core.utils import create_votes


@login_required
@ajax_required
@require_POST
def save_question(request, question_slug):
    data = dict()
    question = get_object_or_404(Question, slug=question_slug)
    user = request.user
    if user not in question.list_users_saved():
        question.users_saved.add(user)
    else:
        question.users_saved.remove(user)
    
    data['html_votes'] = render_to_string('qanda/includes/question_votes.html',
                                        {'question': question},
                                        request=request)

    return JsonResponse(data)


def create_question_votes(request, question_slug, value):
    data = dict()
    question = get_object_or_404(Question, slug=question_slug)
    voted = request.POST.get('voted')
    create_votes(question, request.user, value, voted)

    data['html_votes'] = render_to_string('qanda/includes/question_votes.html',
                                        {'question': question},
                                        request=request)
    return JsonResponse(data)


@login_required
@ajax_required
@require_POST
def voteup_question(request, question_slug):
    return create_question_votes(request, question_slug, True)


@login_required
@ajax_required
@require_POST
def votedown_question(request, question_slug):
    return create_question_votes(request, question_slug, False)


def create_answer_votes(request, question_slug, answer_uuid, value):
    data = dict()
    question = get_object_or_404(Question, slug=question_slug)
    answer = get_object_or_404(Answer, uuid=answer_uuid)
    voted = request.POST.get('voted')
    create_votes(answer, request.user, value, voted)

    data['html_votes'] = render_to_string('qanda/includes/answer_votes.html',
                                        {'answer': answer, 'question': question},
                                        request=request)
    return JsonResponse(data)


@login_required
@ajax_required
@require_POST
def voteup_answer(request, question_slug, answer_uuid):
    return create_answer_votes(request, question_slug, answer_uuid, True)


@login_required
@ajax_required
@require_POST
def votedown_answer(request, question_slug, answer_uuid):
    return create_answer_votes(request, question_slug, answer_uuid, False)



@login_required
@ajax_required
@require_POST
def accept_answer(request, question_slug, answer_uuid):
    data = dict()

    return JsonResponse(data)