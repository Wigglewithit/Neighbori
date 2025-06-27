from django.shortcuts import render
from django.http import JsonResponse
from .models import State, County, City

def location_select_view(request):
    states = State.objects.all()
    return render(request, 'locations/select_location.html', {'states': states})

def load_counties(request):
    state_id = request.GET.get('state_id')
    counties = County.objects.filter(state_id=state_id).order_by('name')
    data = [{'id': county.id, 'name': county.name} for county in counties]
    return JsonResponse(data, safe=False)

def load_cities(request):
    state_id = (
        request.GET.get('state') or
        request.GET.get('id_state') or
        request.GET.get('state_id')
    )

    cities = City.objects.filter(state_id=state_id).order_by('name') if state_id else []

    selected_city_id = request.GET.get('city_id')  # Optional, for editing
    context = {
        'cities': cities,
        'selected_city_id': int(selected_city_id) if selected_city_id else None

    }
    return render(request, 'locations/city_dropdown_list_options.html', context)


def edit_profile_view(request):
    profile, _ = CommunityProfile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profiles:profile_detail', username=request.user.username)
    return render(request, 'profiles/edit_profile.html', {'form': form})
