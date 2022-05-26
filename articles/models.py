from django.db import models
from django.conf import settings

choices = (
    ("science", "science"),
    ("technology", "technology"),
    ("math", "math"),
    ("computers", "computers")
)

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=choices, default='computers')
