from django.shortcuts import render

from .forms import ArticleForm

def home_view(request):
    context = { 
        'form':ArticleForm() 
    }
    return render(request, 'articles/home.html', context)
