from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SkillPostForm
from .models import SkillPost
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create your views here.
def skill_feed(request):
    query = request.GET.get('q')
    post_type = request.GET.get('type')

    posts = SkillPost.objects.all()

    if query:
        posts = posts.filter(
            Q(skill__icontains=query) |
            Q(description__icontains=query)
        )
    if post_type in ['offer', 'request']:
        posts = posts.filter(post_type=post_type)

    # Split tags into lists for display
    for post in posts:
        post.tag_list = [tag.strip() for tag in post.tags.split(',') if tag.strip()]

    return render(request, 'skills/feed.html', {'posts': posts})



@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = SkillPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('skill_feed')
    else:
        form = SkillPostForm()
    return render(request, 'skills/create_post.html', {'form': form})


def skill_detail(request, post_id):
    post = get_object_or_404(SkillPost, id=post_id)
    return render(request, 'skills/detail.html', {'post': post})


