from django.db import models
from django.conf import settings
from django.utils.text import slugify

def user_post_image_path(instance, filename):
    username_slug = slugify(instance.user.username)
    return f"user_posts/{username_slug}/{filename}"

class SkillPost(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('local', 'Local Only'),
        ('connections', 'Connections Only'),
    ]

    POST_TYPE_CHOICES = [
        ('offer', 'Offering a Skill'),
        ('request', 'Requesting a Skill'),
        ('mentorship', 'Offering Mentorship'),
        ('collab', 'Looking to Collaborate'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    skill = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)  # optional title
    description = models.TextField()
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated")
    image = models.ImageField(upload_to=user_post_image_path, blank=True, null=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill} ({self.post_type})"
