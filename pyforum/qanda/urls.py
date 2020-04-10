from django.urls import path

from . import views
from . import views_ajax


urlpatterns = [
    path('new/', views.new_questions, name='new_questions'),
    path('top/', views.top_questions, name='top_questions'),
    path('saved/', views.saved_questions, name='saved_questions'),
    path('unread/', views.unread_questions, name='unread_questions'),
    path('question/<slug:question_slug>/', views.question_detail, name='question_detail'),

    path('ajax/question/<slug:question_slug>/voteup/', views_ajax.voteup_question, name='voteup_question'),
    path('ajax/question/<slug:question_slug>/votedown/', views_ajax.votedown_question, name='votedown_question'),
    path('ajax/question/<slug:question_slug>/save/', views_ajax.save_question, name='save_question'),
]
