from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import TestRun


@receiver(post_save, sender=TestRun)
def delete_cache(sender, instance, **kwargs):
    cache.clear()
