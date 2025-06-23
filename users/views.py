from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Make sure this form exists
from django.contrib.auth import get_user_model

User = get_user_model()
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('skill_feed')  # or wherever you want after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
