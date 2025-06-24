from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model  # ✅ CORRECT
User = get_user_model()
from .models import SkillProfile
from rest_framework import generics, permissions
from .serializers import SkillProfileSerializer
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


def profile_detail_view(request, username):
    profile = get_object_or_404(SkillProfile, user__username=username)
    skills_offered_list = [s.strip() for s in (profile.skills_offered or '').split(',')]
    skills_wanted_list = [s.strip() for s in (profile.skills_wanted or '').split(',')]

    return render(request, 'profiles/profile_detail.html', {
        'profile': profile,
        'skills_offered_list': skills_offered_list,
        'skills_wanted_list': skills_wanted_list
    })

class SkillProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SkillProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


@login_required
def edit_profile_view(request):
    profile, created = SkillProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # ✅ Save is complete — safe to redirect now
            return redirect('profiles:profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})