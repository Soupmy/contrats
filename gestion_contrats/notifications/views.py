from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def mark_as_read(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        notification = Notification.objects.get(pk=pk, utilisateur=request.user)
        notification.lue = True
        notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def mark_all_read(request):
    if request.method == 'POST' and request.user.is_authenticated:
        Notification.objects.filter(utilisateur=request.user, lue=False).update(lue=True)
        return JsonResponse({'status': 'success', 'count': 0})
    return JsonResponse({'status': 'error'}, status=400)