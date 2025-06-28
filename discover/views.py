from django.shortcuts import render
from skills.models import SkillPost
from locations.models import State, City
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from skills.models import SkillPost

    # discover/views.py
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

def discover_api(request):
    skill_type = request.GET.get('skill_type')
    state = request.GET.get('state')
    city = request.GET.get('city')
    page = int(request.GET.get('page', 1))

    posts = SkillPost.objects.filter(visibility='public').order_by('-created_at')

    # Filter by state abbreviation
    if state:
        posts = posts.filter(user__community_profile__state__abbreviation=state)

    # Filter by city name
    if city:
        posts = posts.filter(user__community_profile__city__name=city)

    # Filter by skill

    if skill_type:
        posts = posts.filter(post_type=skill_type)

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    data = [{
        'id': post.id,
        'user': post.user.username,
        'title': post.title,
        'description': post.description,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
        'city': post.user.community_profile.city.name if post.user.community_profile.city else '',
        'state': post.user.community_profile.state.abbreviation if post.user.community_profile.state else '',
    } for post in page_obj]

    return JsonResponse({'posts': data, 'has_next': page_obj.has_next()})

