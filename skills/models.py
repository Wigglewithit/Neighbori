from django.db import models
from django.conf import settings

# Create your models here.

class SkillExchangePost(models.Model):
    POST_TYPE_CHOICES = [
        ('offer', 'Offering a Skill'),
        ('request', 'Requesting a Skill'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    skill = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post_type} - {self.skill}"