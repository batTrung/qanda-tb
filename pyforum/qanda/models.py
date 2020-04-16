from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from core.behaviors import Timestampable, TitleSlugable, UUIDable
from core.models import Category, Voteable
from notifications.constants import ActionTypes
from notifications.utils import create_action

from .managers import AnswerManager, QuestionManager


class Question(UUIDable, TitleSlugable, Timestampable, Voteable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='questions_created')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    users_saved = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='questions_saved')
    users_viewed = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='questions_viewed')
    total_views = models.PositiveIntegerField(default=0)
    objects = QuestionManager()
    
    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('question_detail', args=[self.slug])

    def list_users_viewed(self):
        return self.users_viewed.all()

    def list_users_saved(self):
        return self.users_saved.all()

    def list_unique_users_answered(self):
        return list(set(a.user for a in self.answers.all()))

    def list_unique_users_answered_without_me(self, me):
        result = self.list_unique_users_answered()
        try:
            result.remove(me)
        except ValueError:
            print(f'{ me } not in the list')

        return result

    def top_unique_users_answered(self):
        return self.list_unique_users_answered()[:5]

    def list_answers(self):
        return self.answers.filter(is_reply=False).order_by('-is_answer', '-total_votes')

    def top_answers(self):
        return self.list_answers()[:settings.NUM_ANSWERS]

    @property
    def more_answers(self):
        return self.list_answers().count() > settings.NUM_ANSWERS

    def add_users_viewed(self, user):
        if user.is_authenticated:
            user_exists = self.users_viewed.filter(username=user.username).exists()
            if not user_exists:
                self.users_viewed.add(user)
        return True

    @property
    def count_answers(self):
        return self.answers.count()
    
    @property
    def count_users_saved(self):
        return self.users_saved.count()

    def create_action_save_question(self, actor):
        create_action(self.user, ActionTypes.SAVED, actor, self, self.get_absolute_url())

    def create_action_new_answer(self, actor):
        create_action(self.user, ActionTypes.SAVED, actor, self, self.get_absolute_url())


class Answer(UUIDable, Timestampable, Voteable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='answers_created')
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_answer = models.BooleanField(default=False)
    parent = models.ForeignKey("self",
                            on_delete=models.CASCADE,
                            blank=True,
                            null=True,
                            related_name='replies')
    is_reply = models.BooleanField(default=False, db_index=True)

    objects = AnswerManager()

    def __str__(self):
        return self.content 
        
    def list_replies(self):
        return self.replies.all()
        
    def top_replies(self):
        return self.list_replies()[:settings.NUM_REPLIES]

    @property
    def more_replies(self):
        return self.list_replies().count() > settings.NUM_REPLIES

    @property
    def count_replies(self):
        return self.replies.count()

    def get_absolute_url(self):
        question_detail_url = reverse('question_detail', args=[self.question.slug])
        return f'{ question_detail_url }#item-{self.uuid}'

    def create_action_accept_answer(self, actor):
        if self.is_answer:
            create_action(self.user, ActionTypes.ACCEPTED_ANSWER, actor, self, self.get_absolute_url())
    
    def create_action_new_answer(self, actor):
        pass
