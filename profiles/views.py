from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model  # ✅ CORRECT
User = get_user_model()
from .models import SkillProfile
from rest_framework import generics, permissions
from .serializers import SkillProfileSerializer
from django.contrib.auth.decorators import login_required

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

def edit_profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.bio = request.POST.get("bio", profile.bio)
        profile.skills_offered = request.POST.get("skills_offered", profile.skills_offered)
        profile.skills_wanted = request.POST.get("skills_wanted", profile.skills_wanted)
        profile.trade_preferences = request.POST.get("trade_preferences", profile.trade_preferences)
        profile.save()
        return redirect("edit-profile")  # or wherever you want to go after save

    return render(request, "profiles/edit_profile.html", {"profile": profile})