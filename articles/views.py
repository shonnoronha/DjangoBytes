from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.utils.safestring import mark_safe

from .forms import ArticleForm, ArticleUpdateForm
from .models import Article
from helpers.decorators import verification_required

@login_required
def home_view(request):
    if not request.user.is_email_verified:
        messages.add_message(request,messages.ERROR, mark_safe(f"Please Verify Your Email!<small> <a href='/request-verification' style='color:#842029'>request verification?</a></small>"))
    qs = Article.objects.all()
    context = { 'articles': qs }
    return render(request, 'articles/home.html', context)

@login_required
@verification_required
def create_view(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.add_message(request, messages.SUCCESS, 'Article posted Succesfully!')
            return redirect('articles:home')
        context = { 'form': form }
        return render(request, 'articles/create.html', context)
    context = { 'form': form }
    return render(request, 'articles/create.html', context)

@login_required
@verification_required
def detail_view(request, slug):
    hx_request_url = reverse('articles:hx-detail', kwargs={'slug':slug})
    context = { 'hx_request_url' : hx_request_url }
    return render(request, 'articles/detail.html', context)

@login_required
@verification_required
def hx_detail_view(request, slug):
    if not request.htmx:
        return Http404
    try:
        article = Article.objects.get(slug=slug)
    except Exception:
        return HttpResponse('<h1 class="text-center">Not Found.</h1>')
    context = { 'article': article }
    return render(request, 'articles/partials/detail.html', context)

@login_required
@verification_required
def update_view(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    if instance.author != request.user:
        messages.add_message(request, messages.ERROR, 'Something Went Wrong!!!')
        return redirect(reverse('articles:home'))
    form = ArticleUpdateForm(instance=instance)
    if request.method == 'POST':
        form = ArticleUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Article Updated Succesfully!')
            return redirect('articles:home')
        context = { 'form': form }
        return render(request, 'articles/update.html', context)
    context = { 'form': form }
    return render(request, 'articles/update.html', context)

@login_required
@verification_required
def delete_view(request,id):
    article = get_object_or_404(Article, id=id)
    if article.author != request.user:
        messages.add_message(request, messages.ERROR, 'Something Went Wrong!!!')
        return redirect(reverse('articles:home'))
    if request.method == 'POST':
        article.delete()
        messages.add_message(request, messages.WARNING, 'Article Deleted!')
        if request.htmx:
            headers = {
                "HX-Redirect": reverse('articles:home')
            }
            return HttpResponse('Success', headers=headers)
        return redirect(reverse('articles:home'))
    return render(request, 'articles/delete.html', { 'article':article })