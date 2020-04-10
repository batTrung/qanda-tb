from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse

from ..models import Question, Answer
from ..forms import AnswerForm
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
@require_POST
@ajax_required
def accept_answer(request, question_slug, answer_uuid):
    data = dict()
    question = get_object_or_404(Question, user=request.user, slug=question_slug)
    answer = get_object_or_404(Answer, uuid=answer_uuid)
    question.answers.filter(is_answer=True).update(is_answer=False)
    answer.is_answer = not answer.is_answer
    answer.save()
    data['id_item'] = f'#item-{ answer.uuid }' if answer.is_answer else None

    data['html_votes'] = render_to_string('qanda/includes/answer_votes.html',
                                        {'question': question, 'answer': answer},
                                        request=request)

    return JsonResponse(data)


@login_required
@require_POST
@ajax_required
def create_answer(request, question_slug):
    data = dict()
    question = get_object_or_404(Question, slug=question_slug)
    form = AnswerForm(request.POST)
    if form.is_valid():
        data['is_valid'] = True
        new_answer = form.save(commit=False)
        new_answer.user = request.user
        new_answer.question = question
        new_answer.save()
        data['html_data'] = render_to_string('qanda/answer/item.html',
                                    {'answer': new_answer, 'question': question},
                                    request=request)
    else:
        data['is_valid'] = False

    return JsonResponse(data)


@login_required
@ajax_required
def delete_question(request, question_slug):
    data = dict()
    question = get_object_or_404(Question, user=request.user, slug=question_slug)
    if request.method == "POST":
        question.delete()
        data['redirect_url'] = reverse('new_questions')
    data['html_form'] = render_to_string('qanda/question/form_delete.html',
                                        {'question': question},
                                        request=request)
    return JsonResponse(data)
