from django.urls import path

from .views import question_views, answer_views, ajax_views


urlpatterns = [
    path('new/', question_views.new_questions, name='new_questions'),
    path('top/', question_views.top_questions, name='top_questions'),
    path('saved/', question_views.saved_questions, name='saved_questions'),
    path('unread/', question_views.unread_questions, name='unread_questions'),
    path('question/create/', question_views.create_question, name='create_question'),
    path('question/<slug:question_slug>/', question_views.question_detail, name='question_detail'),
    path('question/category/<slug:category_slug>/', question_views.list_questions_by_category, name='list_questions_by_category'),
    path('question/<slug:question_slug>/update/', question_views.question_update, name='question_update'),

    path('ajax/question/<slug:question_slug>/voteup/', ajax_views.voteup_question, name='voteup_question'),
    path('ajax/question/<slug:question_slug>/votedown/', ajax_views.votedown_question, name='votedown_question'),
    path('ajax/question/<slug:question_slug>/save/', ajax_views.save_question, name='save_question'),
    path('ajax/question/<slug:question_slug>/delete/', ajax_views.delete_question, name='delete_question'),

    path('ajax/question/<slug:question_slug>/answer/<uuid:answer_uuid>/voteup/', ajax_views.voteup_answer, name='voteup_answer'),
    path('ajax/question/<slug:question_slug>/answer/<uuid:answer_uuid>/votedown/', ajax_views.votedown_answer, name='votedown_answer'),
    path('ajax/question/<slug:question_slug>/answer/<uuid:answer_uuid>/accept/', ajax_views.accept_answer, name='accept_answer'),

    path('ajax/question/<slug:question_slug>/answer/create/', ajax_views.create_answer, name='create_answer'),
]
