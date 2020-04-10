from django.urls import reverse
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from .managers import QuestionManager, AnswerManager
from core.behaviors import UUIDable, Timestampable, TitleSlugable
from core.models import Category, Voteable


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
        return list(set(a.user for a in self.answers.all()))[:5]

    def list_answers(self):
        return self.answers.order_by('-is_answer', '-total_votes')

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


class Answer(UUIDable, Timestampable, Voteable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='answers_created')
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_answer = models.BooleanField(default=False)

    objects = AnswerManager()
