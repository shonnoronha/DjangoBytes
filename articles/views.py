from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ArticleForm
from .models import Article

@login_required
def home_view(request):
    qs = Article.objects.all()
    context = { 'articles': qs }
    return render(request, 'articles/home.html', context)

@login_required
def create_view(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        messages.add_message(request, messages.SUCCESS, 'Article posted Succesfully!')
        return redirect('articles:home')
    context = { 'form': form }
    return render(request, 'articles/create.html', context)
