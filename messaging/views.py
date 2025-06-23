from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Max, Q


User = get_user_model()

@login_required
def inbox(request):
    user = request.user

    # Get the most recent message per conversation partner
    latest_messages = (
        Message.objects.filter(Q(sender=user) | Q(recipient=user))
        .order_by('sent_at')  # First sort oldest → newest
    )

    # Use a dict to keep track of only the latest message per conversation partner
    threads = {}
    for message in latest_messages:
        # Get the conversation partner (the other user)
        other_user = message.recipient if message.sender == user else message.sender

        # Always replace with the newer message
        threads[other_user.id] = message

    # Grab just the latest messages
    inbox_messages = list(threads.values())
    inbox_messages.sort(key=lambda m: m.sent_at, reverse=True)  # Most recent first

    return render(request, 'messaging/inbox.html', {
        'inbox_messages': inbox_messages
    })


@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user

            msg.recipient = recipient
            msg.save()
            messages.success(request, f"Message sent to {recipient.username}.")
            return redirect('messages:inbox')
    else:
        form = MessageForm()

    return render(request, 'messaging/compose.html', {
        'form': form,
        'recipient': recipient
    })



@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    return render(request, 'messaging/message_detail.html', {'message': message})
@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk, recipient=request.user)

    if not message.read:
        message.read = True
        message.save()

    return render(request, 'messaging/message_detail.html', {'message': message})

@login_required
def message_thread(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Get all messages between the current user and the other user
    thread_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('sent_at')

    # Mark unread messages from other_user as read
    thread_messages.filter(recipient=request.user, read=False).update(read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.save()
            return redirect('messages:thread', user_id=other_user.id)
    else:
        form = MessageForm()
        form.fields['body'].label = 'Reply'

    return render(request, 'messaging/thread.html', {
        'thread_messages': thread_messages,
        'form': form,
        'recipient': other_user
    })



