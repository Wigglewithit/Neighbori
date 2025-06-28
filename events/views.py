from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EventForm, CommentForm
from .models import Event, RSVP

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('events:list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required
def event_list(request):
    events = Event.objects.all().order_by('date')

    # Optional: add filtering here later (date range, visibility, etc.)
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    has_rsvped = event.rsvps.filter(user=request.user).exists()
    comments = event.comments.order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.event = event
            new_comment.save()
            return redirect('events:detail', pk=event.pk)
    else:
        form = CommentForm()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'has_rsvped': has_rsvped,
        'form': form,
        'comments': comments
    })


@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    already_rsvped = RSVP.objects.filter(event=event, user=request.user).exists()
    if already_rsvped:
        messages.info(request, "You already RSVP'd to this event.")
    else:
        RSVP.objects.create(event=event, user=request.user)
        messages.success(request, "You're going!")

    return redirect('events:detail', pk=pk)
