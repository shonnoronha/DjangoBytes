from django.db import models
from django.conf import settings

from .validators import min_len_validator

choices = (
    ("computers", "computers"),
    ("science", "science"),
    ("technology", "technology"),
    ("math", "math"),
)

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, validators=[min_len_validator])
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=choices, default='computers')
