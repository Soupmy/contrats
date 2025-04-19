from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')[:10],
            'unread_count': Notification.objects.filter(utilisateur=request.user, lue=False).count()
        }
    return {'notifications': [], 'unread_count': 0}