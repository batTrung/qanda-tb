from django.contrib import admin

from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content',)
    list_filter = ('category',)
    search_fields = ('title', 'content',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'content',)
    search_fields = ('content',)

