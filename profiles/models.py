from django.db import models
from django.conf import settings
from locations.models import State, County, ZipCode


class CommunityProfile(models.Model):
    CONNECTION_VISIBILITY = [
        ('public', 'Public'),
        ('connections', 'Connections Only'),
        ('private', 'Private'),
    ]

    LOCATION_SCOPE = [
        ('local', 'Local Only'),
        ('regional', 'Regional'),
        ('global', 'Global'),
    ]
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_profile')

    bio = models.TextField(blank=True)
    skills_offered = models.TextField(blank=True, help_text="Comma-separated list or tags")
    skills_wanted = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    connection_status = models.CharField(max_length=20, choices=CONNECTION_VISIBILITY, default='public')
    location_scope = models.CharField(max_length=20, choices=LOCATION_SCOPE, default='regional')

    region = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    counties = models.ManyToManyField(County, blank=True)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, null=True, blank=True)

    available_for = models.TextField(blank=True, help_text="e.g., mentoring, collaboration, barter")

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_mentor = models.BooleanField(default=False)
    allow_lurkers = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Community Profile"

class Testimonial(models.Model):
    profile = models.ForeignKey('CommunityProfile', on_delete=models.CASCADE, related_name='testimonials')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author.username} for {self.profile.user.username}"