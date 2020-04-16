from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST

from core.decorators import ajax_required
from core.helpers import get_pagination_items
from core.utils import create_votes

from ..forms import AnswerForm, ReplyForm
from ..models import Answer, Question


@login_required
@ajax_required
@require_POST
def save_question(request, question_slug):
    data = dict()
    question = get_object_or_404(Question, slug=question_slug)
    user = request.user
    if user not in question.list_users_saved():
        question.users_saved.add(user)
        question.create_action_save_question(request.user)
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
    answer.create_action_accept_answer(request.user)
    
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
                                    {'answer': new_answer, 'question': question, 'reply_form': ReplyForm()},
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


@login_required
@ajax_required
def delete_answer(request, answer_uuid):
    data = dict()
    answer = get_object_or_404(Answer, user=request.user, uuid=answer_uuid)
    if request.method == "POST":
        data['id_item'] = f'#item-{answer.uuid}'
        answer.delete()
    else:
        data['html_form'] = render_to_string('qanda/answer/form_delete.html',
                                            {'answer': answer},
                                            request=request)
    return JsonResponse(data)


@login_required
@ajax_required
def update_answer(request, answer_uuid):
    data = dict()
    answer = get_object_or_404(Answer, user=request.user, uuid=answer_uuid)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            data['is_valid'] = True
            data['id_item'] = f'#item-{answer.uuid}'
            case = 'reply' if answer.is_reply else 'answer'
            data['html_data'] = render_to_string(f'qanda/{case}/item.html',
                                                {f'{case}': answer, 'reply_form': ReplyForm()},
                                                request=request)
        else:
            data['is_valid'] = False

    else:
        form = AnswerForm(instance=answer)

    data['html_form'] = render_to_string('qanda/answer/form_update.html',
                                        {'answer': answer, 'form': form},
                                        request=request)
    return JsonResponse(data)


@login_required
@require_POST
@ajax_required
def create_reply(request, answer_uuid):
    data = dict()
    answer = get_object_or_404(Answer, uuid=answer_uuid)
    form = ReplyForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        content = cd['content']
        new_reply = Answer(
            user=request.user,
            content=content,
            parent=answer,
            question=answer.question,
            is_reply=True)
        new_reply.save()
        data['is_valid'] = True
        data['html_data'] = render_to_string('qanda/reply/item.html',
                                            {'reply': new_reply},
                                            request=request)
    else:
        data['is_valid'] = False

    data['html_form'] = render_to_string('qanda/reply/form_create.html',
                                        {'form': form, 'answer': answer},
                                        request=request)
    return JsonResponse(data)


@ajax_required
def load_more_asnwers(request, question_slug):
    data = dict()
    question = get_object_or_404(Question, slug=question_slug)
    answers = get_pagination_items(request, question.list_answers(), settings.NUM_ANSWERS)
    if answers:
        data['is_valid'] = True
        data['html_data'] = render_to_string('qanda/answer/list.html',
                                            {"answers": answers, 'reply_form': ReplyForm()},
                                            request=request)
    else:
        data['is_valid'] = False

    return JsonResponse(data)


@ajax_required
def load_more_replies(request, answer_uuid):
    data = dict()
    answer = get_object_or_404(Answer, uuid=answer_uuid)
    replies = get_pagination_items(request, answer.list_replies(), settings.NUM_REPLIES)
    if replies:
        data['is_valid'] = True
        data['html_data'] = render_to_string('qanda/reply/list.html',
                                            {"replies": replies},
                                            request=request)
    else:
        data['is_valid'] = False

    return JsonResponse(data)
