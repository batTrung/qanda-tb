from collections import Counter

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from notifications.constants import ActionTypes
from notifications.utils import create_action

from .behaviors import TitleSlugable, UUIDable
from .managers import VoteManager


class Category(TitleSlugable):
    pass

    class Meta:
        verbose_name_plural = "Categories"


class Vote(UUIDable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    value = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = VoteManager()

    class Meta:
        unique_together = (
            "user",
            "content_type",
            "object_id",
        )

    def save(self, *args, **kwargs):
        super(Vote, self).save(*args, **kwargs)
        if self.content_object.user != self.user:
            verb = ActionTypes.VOTED_UP if self.value else ActionTypes.VOTED_DOWN
            create_action(
                self.content_object.user, verb, self.user, self.content_object, self.content_object.get_absolute_url()
            )


class Voteable(models.Model):
    total_votes = models.IntegerField(default=0, db_index=True)
    votes = GenericRelation(Vote)

    def count_votes(self):
        dic = Counter(self.votes.values_list("value", flat=True))
        type(self).objects.filter(uuid=self.uuid).update(total_votes=dic[True] - dic[False])
        self.refresh_from_db()

    def count_votes_up(self):
        return self.votes.filter(value=False).count()

    def list_users_voteup(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def list_users_votedown(self):
        return [vote.user for vote in self.votes.filter(value=False)]

    class Meta:
        abstract = True
