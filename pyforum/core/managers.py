from django.db import models


class CommentManager(models.Manager):
    def get_queryset(self):
        return super(CommentManager,
            self).get_queryset(
            ).select_related('user',
            )

class VoteManager(models.Manager):
    def get_queryset(self):
        return super(VoteManager,
            self).get_queryset(
            ).select_related('user'
            )
