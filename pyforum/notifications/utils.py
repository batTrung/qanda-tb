import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Action


def create_action(recipient, verb, actor=None, content_object=None, link=None):
    if recipient != actor:
        now = timezone.now()
        last_minute = now - datetime.timedelta(seconds=60)

        similar_actions = Action.objects.filter(recipient=recipient, verb=verb, created_at__gte=last_minute)
        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            similar_actions = similar_actions.filter(content_type=content_type, object_id=content_object.pk)

        if not similar_actions:
            print("NO SIMILAR Actions")
            new_action = Action(recipient=recipient, verb=verb, actor=actor, link=link, content_object=content_object)
            new_action.save()
            return True

    return False
