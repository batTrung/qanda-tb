from django.db import models


class QuestionManager(models.Manager):
    def get_queryset(self):
        return (
            super(QuestionManager, self)
            .get_queryset()
            .select_related("user", "category",)
            .prefetch_related("answers", "users_viewed", "answers__user",)
        )

    def list_unread_answers(self, user):
        query = self.get_queryset()
        return query.exclude(users_viewed__in=[user.id])

    def list_saved_answers(self, user):
        query = self.get_queryset()
        return query.filter(users_saved__in=[user.id])


class AnswerManager(models.Manager):
    def get_queryset(self):
        return super(AnswerManager, self).get_queryset().select_related("user",).prefetch_related("replies")
