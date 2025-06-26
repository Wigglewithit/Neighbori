from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from django.contrib.auth.decorators import login_required

from .models import CommunityProfile
from .forms import ProfileForm
from .serializers import SkillProfileSerializer
from skills.models import SkillPost
from locations.models import State, City

User = get_user_model()


@login_required
def my_profile(request):
    return redirect('profiles:profile_detail', username=request.user.username)


def profile_detail(request, username):
    user_profile = get_object_or_404(User, username=username)
    skill_posts = SkillPost.objects.filter(user=user_profile).order_by('-created_at')
    profile = CommunityProfile.objects.filter(user=user_profile).first()

    skills_offered_list = [s.strip() for s in profile.skills_offered.split(',')] if profile and profile.skills_offered else []
    skills_wanted_list = [s.strip() for s in profile.skills_wanted.split(',')] if profile and profile.skills_wanted else []

    # Clean up tag strings for display
    for post in skill_posts:
        post.tag_list = [tag.strip() for tag in post.tags.split(',')] if post.tags else []

    return render(request, 'profiles/profile_detail.html', {
        'user_profile': user_profile,
        'skill_posts': skill_posts,
        'profile': profile,
        'skills_offered_list': skills_offered_list,
        'skills_wanted_list': skills_wanted_list,
    })


@login_required
def edit_profile_view(request):
    profile, _ = CommunityProfile.objects.get_or_create(user=request.user)

    # Use POST or GET data to allow proper state dropdown selection before form save
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST':
        print("POST data received:", request.POST)

        if form.is_valid():
            form.save()
            print("Profile saved for:", request.user.username)
            return redirect('profiles:profile_detail', username=request.user.username)
        else:
            print("Form errors:", form.errors)
    else:
        print("Rendering form for GET request.")

    states = State.objects.all().order_by('abbreviation')

    return render(request, 'profiles/edit_profile.html', {
        'form': form,
        'profile': profile,
        'states': states,
    })


class SkillProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SkillProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


def user_directory(request):
    search_query = request.GET.get("q", "")
    state = request.GET.get("state", "")
    county = request.GET.get("county", "")
    gender = request.GET.get("gender", "")
    min_age = request.GET.get("min_age", "")
    max_age = request.GET.get("max_age", "")
    age = request.GET.get("age", "")

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
        profiles = profiles.filter(gender__iexact=gender)
    if min_age:
        profiles = profiles.filter(age__gte=min_age)
    if max_age:
        profiles = profiles.filter(age__lte=max_age)
    if state:
        profiles = profiles.filter(city__state__name__icontains=state)  # Updated for new City-State setup
    if age:
        profiles = profiles.filter(age=age)  # if you implement age_group, tweak accordingly

    return render(request, "profiles/user_directory.html", {
        "profiles": profiles.distinct(),
        "search_query": search_query,
        "state": state,
        "age": age,
        "gender": gender,
        "min_age": min_age,
        "max_age": max_age,
    })
