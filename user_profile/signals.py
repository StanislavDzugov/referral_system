from user_profile.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=CustomUser)
def create_customer(sender, instance, created, **kwargs):
    """Create UserProfile after we create User"""

    if created:
        UserProfile.objects.create(user=instance)
