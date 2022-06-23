from random import randint
from django.utils.text import slugify

def slugify_name(instance, save=True, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    if instance.__class__.objects.filter(slug=slug).exclude(id=instance.id).exists():
        slug = f'{slug}-{randint(1, 100_000)}'
        return slugify_name(instance, save, slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance