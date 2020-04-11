from django.db import models


class VoteManager(models.Manager):
    def get_queryset(self):
        return super(VoteManager,
            self).get_queryset(
            ).select_related('user'
            )

    def count_voteup(self):
        return self.get_queryset().filter(value=True).count()

    def count_votedown(self):
        return self.get_queryset().filter(value=False).count()

