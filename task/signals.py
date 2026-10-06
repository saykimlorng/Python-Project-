from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Profile)
def update_user_from_profile(sender, instance, **kwargs):
    """Copy profile contact information to the related user record."""
    user = instance.user
    changed_fields = []

    for field_name in ('phone', 'address', 'bio'):
        if not hasattr(user, field_name):
            continue

        profile_value = getattr(instance, field_name)
        if getattr(user, field_name) != profile_value:
            setattr(user, field_name, profile_value)
            changed_fields.append(field_name)

    if changed_fields:
        user.save(update_fields=changed_fields)


# alter warning
@receiver(post_save, sender=User)
def create_profile_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Profile.objects.get_or_create(user=instance)
        if not instance.profile.phone:
            print("\n⚠️  Remember to set a phone number for this superuser!\n")