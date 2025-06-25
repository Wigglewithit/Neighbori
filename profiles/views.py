from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import CommunityProfile
from rest_framework import generics, permissions
from .serializers import SkillProfileSerializer
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from skills.models import SkillPost

User = get_user_model()

@login_required
def my_profile(request):
    return redirect('profiles:profile_detail', username=request.user.username)


def profile_detail(request, username):
    user_profile = get_object_or_404(User, username=username)
    skill_posts = SkillPost.objects.filter(user=user_profile).order_by('-created_at')
    profile = CommunityProfile.objects.filter(user=user_profile).first()

    # Clean up tag strings for display
    for post in skill_posts:
        post.tag_list = [tag.strip() for tag in post.tags.split(',')] if post.tags else []

    return render(request, 'profiles/profile_detail.html', {
        'user_profile': user_profile,
        'skill_posts': skill_posts,
        'profile': profile,
    })


class SkillProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SkillProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


@login_required
def edit_profile_view(request):
    profile, created = CommunityProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print("POST data received:", request.POST)  # See what was submitted

        if form.is_valid():
            form.save()
            print("Profile saved for:", request.user.username)
            return redirect('profiles:profile_detail', username=request.user.username)
        else:
            print("Form errors:", form.errors)  # ADD THIS LINE
    else:
        print("Rendering form for GET request.")
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})

User = get_user_model()

def user_directory(request):
    search_query = request.GET.get("q", "")
    state = request.GET.get("state", "")
    county = request.GET.get("county", "")
    gender = request.GET.get("gender", "")
    min_age = request.GET.get("min_age", "")
    max_age = request.GET.get("max_age", "")
    age = request.GET.get("age", "")  # Optional, if you're supporting age groups

    profiles = CommunityProfile.objects.select_related("user").all()

    if search_query:
        profiles = profiles.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(skills_offered__icontains=search_query)
        )

    if gender:
        profiles = profiles.filter(user__community_profile__gender__iexact=gender)

    if min_age:
        profiles = profiles.filter(user__community_profile__age__gte=min_age)

    if max_age:
        profiles = profiles.filter(user__community_profile__age__lte=max_age)

    if state:
        profiles = profiles.filter(region__name__icontains=state)

    if county:
        profiles = profiles.filter(counties__name__icontains=county)

    # Only if you support `age_group` on user.profile
    if age:
        profiles = profiles.filter(user__profile__age_group=age)

    return render(request, "profiles/user_directory.html", {
        "profiles": profiles.distinct(),
        "search_query": search_query,
        "state": state,
        "county": county,
        "age": age,
        "gender": gender,
        "min_age": min_age,
        "max_age": max_age,
    })




