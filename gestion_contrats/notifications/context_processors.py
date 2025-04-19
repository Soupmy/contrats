from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
        unread_count = notifications.filter(lue=False).count()
        return {
            'notifications': notifications,
            'unread_count': unread_count
        }
    return {}
