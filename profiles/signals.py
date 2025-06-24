from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import CommunityProfile
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_community_profile(sender, instance, created, **kwargs):
    if created:
        CommunityProfile.objects.create(user=instance)