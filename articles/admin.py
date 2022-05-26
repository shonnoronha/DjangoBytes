from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'date_added']
    search_fields = ['description', 'content', 'name']
    readonly_fields = ['date_added']
