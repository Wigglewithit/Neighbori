from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SkillPostForm
from .models import SkillPost
from django.db.models import Q
from django.shortcuts import get_object_or_404



# Create your views here.
def skill_feed(request):
    posts = SkillPost.objects.all()

    query = request.GET.get("q")
    post_type = request.GET.get("type")
    tag = request.GET.get("tag")

    if query:
        posts = posts.filter(description__icontains=query)
    if post_type:
        posts = posts.filter(post_type=post_type)
    if tag:
        posts = posts.filter(tags__icontains=tag)

    for post in posts:
        post.tag_list = [t.strip() for t in post.tags.split(",") if t.strip()]

    return render(request, "skills/feed.html", {"posts": posts})



@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = SkillPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.profile = request.user.community_profile  # ✅ Add this
            post.save()
            return redirect('skill_feed')
    else:
        form = SkillPostForm()
    return render(request, 'skills/create_post.html', {'form': form})


def skill_detail(request, post_id):
    post = get_object_or_404(SkillPost, id=post_id)
    return render(request, 'skills/detail.html', {'post': post})


