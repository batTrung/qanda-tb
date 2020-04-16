from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="users/", blank=True, null=True)

    @property
    def get_word_avatar(self):
        if self.first_name and self.last_name:
            return "".join((self.first_name[0], self.last_name[0])).upper()
        else:
            return self.username[0].upper()
