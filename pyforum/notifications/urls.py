from django.urls import path

from . import views

urlpatterns = [
    path("ajax/notificatios/", views.get_actions, name="get_actions"),
    path("ajax/notificatios/mark-all-as-read/", views.mark_all_as_read, name="mark_all_as_read"),
    path("ajax/action/<uuid:action_uuid>/mark-action-as-read/", views.mark_action_as_read, name="mark_action_as_read"),
]
