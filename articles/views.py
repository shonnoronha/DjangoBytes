from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ArticleForm

def home_view(request):
    print(request.method)
    return render(request, 'articles/home.html', {})
    
def create_view(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        messages.add_message(request, messages.SUCCESS, 'Article posted Succesfully!')
        return redirect('articles:home')
    context = { 'form': form }
    return render(request, 'articles/create.html', context)
