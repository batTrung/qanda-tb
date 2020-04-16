from django.db import models


class ActionManager(models.Manager):
    def get_queryset(self):
        return super(ActionManager, self).get_queryset().select_related("actor")
