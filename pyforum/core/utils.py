import random

from django.db.models import Max
from django.contrib.contenttypes.models import ContentType

from .models import Vote


def get_random_obj(cls):
    max_id = cls.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        category = cls.objects.filter(pk=pk).first()
        if category:
            return category


def create_votes(obj, user, value, voted):
    ct = ContentType.objects.get_for_model(obj)
    vote = Vote.objects.filter(content_type=ct, user=user, object_id=obj.uuid)
    if voted == "TRUE":
        vote.delete()
    else:
        vote, created = obj.votes.update_or_create(user=user, defaults={"value": value})
        
    obj.count_votes()
