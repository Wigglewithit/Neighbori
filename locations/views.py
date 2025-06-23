from django.shortcuts import render
from django.http import JsonResponse
from .models import State, County, ZipCode

def location_select_view(request):
    states = State.objects.all()
    return render(request, 'locations/select_location.html', {'states': states})

def load_counties(request):
    state_id = request.GET.get('state_id')
    counties = County.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(counties), safe=False)

def load_zipcodes(request):
    county_id = request.GET.get('county_id')
    zips = City.objects.filter(county_id=county_id).values('zipcode')
    return JsonResponse(list(zips), safe=False)
