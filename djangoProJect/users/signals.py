from django.db.models.signals import post_save
# ^ the signal that gets fired after an obj is saved
from django.contrib.auth.models import User
# ^ the sender model
from django.dispatch import receiver
# the receiver model
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# ^^^^ runs every time a user is created

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # **kwargs -> accepts any additional keyword argument
    instance.profile.save()