#signals.py


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile created for user:", instance.username)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
            print("Profile saved for user:", instance.username)
        else:
            Profile.objects.create(user=instance)
            print("Profile created for user on save:", instance.username)