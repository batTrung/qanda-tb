from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Question
from core.helpers import get_pagination_items



def list_questions(request, query, section=''):
    questions = get_pagination_items(request, query)
    if request.is_ajax():
        data = dict()
        if questions:
            data['is_valid'] = True
            data['html_data'] =  render_to_string('qanda/includes/list_questions.html',
                                                {'questions': questions},
                                                request=request)
            id_item = f'#q-{ questions[0].slug }'
            data['id_item'] = id_item
        else:
            data['is_valid'] = False
        return JsonResponse(data)

    context = {
        'questions': questions,
        'section': section,
    }
    return render(request, 'qanda/question/list.html', context)


def new_questions(request):
    query = Question.objects.all()
    return list_questions(request, query, 'new')


def top_questions(request):
    query = Question.objects.order_by('-total_votes', '-total_views')
    return list_questions(request, query, 'top')


@login_required
def saved_questions(request):
    query = Question.objects.list_saved_answers(request.user)
    return list_questions(request, query, 'saved')


@login_required
def unread_questions(request):
    query = Question.objects.list_unread_answers(request.user)
    return list_questions(request, query, 'unread')


def question_detail(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug)
    question.add_users_viewed(request.user)
    
    session_key = 'viewed_question_{}'.format(question.pk)
    if not request.session.get(session_key, False):
        question.total_views += 1
        question.save()
        request.session[session_key] = True

    context = {
        'question': question,
        'section': 'new',
    }

    return render(request, 'qanda/question/detail.html', context)
