from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.utils import generate_random_string
from .models import Article


@receiver(pre_save, sender=Article)
def creation_slug_to_article(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255
    SALT_SIZE = 4

    def create_slug():
        base = slugify(instance.title or '')[:MAXIMUM_SLUG_LENGTH - SALT_SIZE]
        if not base:
            base = generate_random_string(8)

        unique = generate_random_string(SALT_SIZE)
        candidate = f"{base}-{unique}"
        candidate = slugify(candidate)[:MAXIMUM_SLUG_LENGTH]

        qs = sender.objects.filter(slug=candidate)
        qs = qs.exclude(pk=instance.pk)

        while qs.exists():
            unique = generate_random_string(SALT_SIZE)
            candidate = slugify(f"{base}-{unique}")[:MAXIMUM_SLUG_LENGTH]
            qs = sender.objects.filter(slug=candidate)
            qs = qs.exclude(pk=instance.pk)

        instance.slug = candidate

    if getattr(instance, '_state', None) and instance._state.adding:
        create_slug()
        return None
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return None

    if old_instance.title == instance.title:
        return None

    create_slug()