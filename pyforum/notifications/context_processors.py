def notifications(request):
    print("is_running")
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_seen=False).count()
        return {
            'count_notifications': count
        }
    else:
        return dict()
