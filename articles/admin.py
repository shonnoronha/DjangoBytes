from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'date_added']
    search_fields = ['description', 'content', 'name']
    readonly_fields = ['date_added', 'date_edited']

    def save_model(self, request, obj, form , change):
        update_fields = []
        if form.initial['name'] != form.cleaned_data['name']:
            update_fields.append('name')
        obj.save(update_fields=update_fields)
        super().save_model(request, obj, form, change)
