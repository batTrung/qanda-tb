from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from core.models import Category
from core.helpers import get_pagination_items


def list_categories(request):
    query = Category.objects.annotate(
        num_questions = Count('questions')
    ).order_by('-num_questions')
    categories = get_pagination_items(request, query)

    if request.is_ajax():
        data = dict()
        if categories:
            data["is_valid"] = True
            data["html_data"] = render_to_string(
                "qanda/category/categories.html",
                {
                    "categories": categories,
                },
                request=request
            )
            id_item = f"#q-{ categories[0].slug }"
            data["id_item"] = id_item
        else:
            data["is_valid"] = False
        return JsonResponse(data)

    return render(
        request,
        "qanda/category/list.html",
        {
            "categories": categories,
            "section": "categories",
        }
    )
