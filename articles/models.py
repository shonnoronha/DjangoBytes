from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse
from PIL import Image

from .validators import min_len_validator
from .utils import slugify_name

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.CharField(max_length=200, validators=[min_len_validator])
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='thumbnail/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug':self.slug})
    
    def get_update_url(self):
        return reverse('articles:update', kwargs={'slug':self.slug})
    
    def get_delete_url(self):
        return reverse('articles:delete', kwargs={'id': self.id})

def article_post_save(sender, instance, created, update_fields ,*args, **kwargs):
    if created:
        slugify_name(instance, True)
        if instance.thumbnail: # resize image before saving
            img = Image.open(instance.thumbnail.path)
            if (img.height > 300) or (img.width > 300):
                img.thumbnail((300, 300))
                img.save(instance.thumbnail.path)
    if update_fields:
        if 'name' in update_fields:
            slugify_name(instance, True)
    
post_save.connect(article_post_save, sender=Article)