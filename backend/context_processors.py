from messaging.models import Message

def unread_message_count(request):
    try:
        if request.user.is_authenticated:
            count = Message.objects.filter(recipient=request.user, read=False).count()
            return {'unread_message_count': count}
    except Exception:
        pass
    return {'unread_message_count': 0}
