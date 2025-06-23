from django.db import models
from django.conf import settings
from locations.models import State, County, ZipCode


class SkillProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # Basic info
    bio = models.TextField(blank=True)
    skills_offered = models.TextField(help_text="Comma-separated list of skills you're offering")
    skills_wanted = models.TextField(help_text="Comma-separated list of skills you want to learn")

    # Location fields
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    counties = models.ManyToManyField(County, blank=True)
    city = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, null=True, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    search_radius = models.IntegerField(default=10, help_text="Search radius in miles for feed")

    # New fields
    TRADE_CHOICES = [
        ('services', 'Services'),
        ('items', 'Items'),
        ('projects', 'Projects'),
        ('mentorship', 'Mentorship'),
    ]
    trade_preferences = models.CharField(max_length=50, choices=TRADE_CHOICES, default='services')
    allow_lurkers = models.BooleanField(default=False)
    open_to_connections = models.BooleanField(default=True)
    availability = models.JSONField(blank=True, null=True, help_text="Store availability info like time blocks")

    def __str__(self):
        return f"{self.user.username}'s Skill Profile"

class Testimonial(models.Model):
    profile = models.ForeignKey(SkillProfile, on_delete=models.CASCADE, related_name='testimonials')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author.username} for {self.profile.user.username}"
