from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from core.decorators import ajax_required
from core.helpers import get_pagination_items

from .models import Action


def get_list_actions(request, query):
    data = dict()
    actions = get_pagination_items(request, query, settings.NUMBER_ACTIONS)
    if actions:
        data['is_valid'] = True
        data['html_data'] = render_to_string(
                                'notifications/list.html',
                                {'actions': actions},
                                request=request)
    else:
        data['is_valid'] = False

    return JsonResponse(data)


@login_required
@ajax_required
def get_actions(request):
    query = request.user.notifications.all()
    query.update(is_seen=True)
    return get_list_actions(request, query)


@login_required
@ajax_required
@require_POST
def mark_all_as_read(request):
    query = request.user.notifications.all()
    query.update(is_read=True)
    return get_list_actions(request, query)


@login_required
@ajax_required
@require_POST
def mark_action_as_read(request, action_uuid):
    data = dict()
    action = get_object_or_404(Action, uuid=action_uuid, recipient=request.user)
    action.is_read = True
    action.save()
    if action.link:
        data['is_valid'] = True
        data['redirect_url'] = action.link
    else:
        data['is_valid'] = False

    return JsonResponse(data)
