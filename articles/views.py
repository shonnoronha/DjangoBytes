from django.shortcuts import render

from .forms import ArticleForm

def home_view(request):
    return render(request, 'articles/home.html', { 'form':ArticleForm() })
