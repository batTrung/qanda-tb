from collections import Counter

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .behaviors import UUIDable, TitleSlugable
from .managers import VoteManager


class Category(TitleSlugable):
    pass

    class Meta:
        verbose_name_plural = 'Categories'


class Vote(UUIDable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='+')
    value = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id',)


class Voteable(models.Model):
    total_votes = models.IntegerField(default=0)
    votes = GenericRelation(Vote)

    def count_votes(self):
        dic = Counter(self.votes.values_list("value", flat=True))
        type(self).objects.filter(uuid=self.uuid).update(total_votes=dic[True] - dic[False])
        self.refresh_from_db()

    def list_users_voteup(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def list_users_votedown(self):
        return [vote.user for vote in self.votes.filter(value=False)]

    class Meta:
        abstract = True
