from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model  # ✅ CORRECT
User = get_user_model()
from .models import CommunityProfile
from rest_framework import generics, permissions
from .serializers import SkillProfileSerializer
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from skills.models import SkillPost




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
            print("✅ Profile saved for:", request.user.username)
            return redirect('profiles:profile_detail', username=request.user.username)
        else:
            print("❌ Form errors:", form.errors)  # ADD THIS LINE
    else:
        print("Rendering form for GET request.")
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})





