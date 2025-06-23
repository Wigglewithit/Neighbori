from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SkillExchangePostForm
from .models import SkillExchangePost
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Create your views here.
def skill_feed(request):
    query = request.GET.get('q')
    post_type = request.GET.get('type')

    posts = SkillExchangePost.objects.all()

    if query:
        posts = posts.filter(
            Q(skill__icontains=query) |
            Q(description__icontains=query)
        )
    if post_type in ['offer', 'request']:
        posts = posts.filter(post_type=post_type)

    return render(request, 'skills/feed.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = SkillExchangePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('skill_feed')
    else:
        form = SkillExchangePostForm()

    return render(request, 'skills/create_post.html', {'form': form})  # ✅ Always returns this


def skill_detail(request, post_id):
    post = get_object_or_404(SkillExchangePost, id=post_id)
    return render(request, 'skills/detail.html', {'post': post})

