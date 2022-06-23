from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse

from .validators import min_len_validator
from .utils import slugify_name

choices = (
    ("computers", "computers"),
    ("science", "science"),
    ("technology", "technology"),
    ("math", "math"),
)

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.CharField(max_length=200, validators=[min_len_validator])
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=50, choices=choices, default='computers')

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'id':self.id})

def article_post_save(sender, instance, created, update_fields ,*args, **kwargs):
    if created:
        slugify_name(instance, True)
    if update_fields:
        if 'name' in update_fields:
            slugify_name(instance, True)
    
post_save.connect(article_post_save, sender=Article)