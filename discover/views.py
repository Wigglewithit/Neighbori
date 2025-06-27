from django.shortcuts import render
from skills.models import SkillPost
from locations.models import State, City
from django.db.models import Q

def feed(request):
    # Get filter values from request
    state_id = request.GET.get('state')
    city_id = request.GET.get('city')
    skill_type = request.GET.get('skill_type')  # 'offered' or 'requested'
    search_query = request.GET.get('search')

    # Start with all public posts
    posts = SkillPost.objects.filter(visibility='public').order_by('-created_at')

    # Apply state filter
    if state_id:
        posts = posts.filter(user__community_profile__state_id=state_id)


    # Apply city filter
    if city_id:
        posts = posts.filter(user__community_profile__city_id=city_id)


    # Apply skill type filter
    if skill_type == 'offered':
        posts = posts.filter(post_type='offer')
    elif skill_type == 'requested':
        posts = posts.filter(post_type='request')

    # Apply search filter
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # For filter dropdowns
    states = State.objects.all().order_by('name')
    cities = City.objects.filter(state_id=state_id).order_by('name') if state_id else City.objects.none()

    context = {
        'posts': posts,
        'states': states,
        'cities': cities,
        'selected_state': state_id,
        'selected_city': city_id,
        'selected_type': skill_type,
        'search_query': search_query
    }
    return render(request, 'discover/feed.html', context)
