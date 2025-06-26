from django.db import models
from django.conf import settings
from locations.models import State, County, City


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

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('nonbinary', 'Non-binary'),
        ('other', 'Other'),
        ('prefer_not', 'Prefer not to say'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_profile')

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    skills_offered = models.TextField(blank=True, help_text="Comma-separated list or tags")
    skills_wanted = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    connection_status = models.CharField(max_length=20, choices=CONNECTION_VISIBILITY, default='public')
    location_scope = models.CharField(max_length=20, choices=LOCATION_SCOPE, default='regional')

    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    counties = models.ManyToManyField(County, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)


    available_for = models.TextField(blank=True, help_text="e.g., mentoring, collaboration, barter")
    is_mentor = models.BooleanField(default=False)
    allow_lurkers = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # If a city is selected, auto-set state and counties
        if self.city:
            self.state = self.city.state
            super().save(*args, **kwargs)

            # Match county using the city's associated county (recommended)
            if self.city.county:
                self.counties.set([self.city.county])
            else:
                self.counties.clear()
        else:
            # No city selected; just save and clear counties
            super().save(*args, **kwargs)
            self.counties.clear()

    def __str__(self):
        return f"{self.user.username}'s Community Profile"


class Testimonial(models.Model):
    profile = models.ForeignKey('CommunityProfile', on_delete=models.CASCADE, related_name='testimonials')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author.username} for {self.profile.user.username}"