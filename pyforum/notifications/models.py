from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import mark_safe

from core.behaviors import UUIDable

from .constants import ActionTypes
from .managers import ActionManager


class Action(UUIDable):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name="notifications_created"
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    verb = models.CharField(max_length=2, choices=ActionTypes.CHOICES)
    link = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100, blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = ActionManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        if self.content_object:
            return mark_safe(
                f"""
                        <b>{self.actor}</b>
                        {self.get_verb_display()}{self.content_object.__class__.__name__}:
                        {self.content_object}
                        """
            )
        else:
            return mark_safe(f"{self.get_verb_display()}")

    @property
    def get_icon(self):
        icons = {
            ActionTypes.VOTED_UP: "text-primary fa-arrow-up",
            ActionTypes.VOTED_DOWN: "text-danger fa-arrow-down",
            ActionTypes.ANSWERED: "text-primary fa-comment",
            ActionTypes.ALSO_ANSWERED: "text-success fa-comments",
            ActionTypes.COMMENTED: "text-success fa-comment",
            ActionTypes.ACCEPTED_ANSWER: "text-success fa-check",
            ActionTypes.SAVED: "text-warning fa-star",
        }
        return icons.get(self.verb, "")
