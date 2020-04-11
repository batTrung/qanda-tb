import uuid
import string
import random

from django.utils.text import slugify
from django.db import models


class UUIDable(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
        

class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,  db_index=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True


class TitleSlugable(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250,
                            db_index=True,
                            unique=True,
                            blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            hext = ''.join(random.choice(string.hexdigits) for i in range(5))
            self.slug = '-'.join((slug, hext))
        super(TitleSlugable, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


