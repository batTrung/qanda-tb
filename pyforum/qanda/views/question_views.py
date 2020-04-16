from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from core.helpers import get_pagination_items

from ..forms import AnswerForm, QuestionForm, ReplyForm
from ..models import Question


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


def list_questions_by_category(request, category_slug):
    query = Question.objects.filter(category__slug=category_slug)
    return list_questions(request, query)


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
        'reply_form': ReplyForm(),
        'form': AnswerForm(),
        'section': 'new',
    }

    return render(request, 'qanda/question/detail.html', context)


@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.user = request.user
            new_question.save()
            return redirect(reverse('question_detail', args=[new_question.slug]))
    else:
        form = QuestionForm()

    context = {
        'form': form,
    }
    return render(request, 'qanda/question/create.html', context)


@login_required
def question_update(request, question_slug):
    question = get_object_or_404(Question, user=request.user, slug=question_slug)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question_detail', args=[question.slug]))
    else:
        form = QuestionForm(instance=question)
        
    context = {
        'form': form,
    }
    return render(request, 'qanda/question/update.html', context)
