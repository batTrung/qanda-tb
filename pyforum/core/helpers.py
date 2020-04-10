import random

from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_random_obj(cls):
    max_id = cls.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        category = cls.objects.filter(pk=pk).first()
        if category:
            return category


def get_pagination_items(request, query, num=30):
    paginator = Paginator(query, num)
    page = request.GET.get('page', 1)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return ''
        results = paginator.page(paginator.num_pages)

    return results

