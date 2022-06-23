from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import Http404

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
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.add_message(request, messages.SUCCESS, 'Article posted Succesfully!')
        return redirect('articles:home')
    context = { 'form': form }
    return render(request, 'articles/create.html', context)

@login_required
def detail_view(request, slug):
    hx_request_url = reverse('articles:hx-detail', kwargs={'slug':slug})
    context = { 'hx_request_url' : hx_request_url }
    return render(request, 'articles/detail.html', context)

@login_required
def hx_detail_view(request, slug):
    if not request.htmx:
        return Http404
    article = get_object_or_404(Article, slug=slug)
    context = { 'article': article }
    return render(request, 'articles/partials/detail.html', context)