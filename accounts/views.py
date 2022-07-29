from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignInForm

def base_view(request):
    return redirect(reverse('articles:home'))

def login_view(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_email_verified:
                messages.add_message(request, messages.ERROR, f'Please Verify Your Email Sent To `{user.email}`')
                return render(request, 'accounts/verify.html')
            login(request, form.get_user())
            messages.add_message(request, messages.SUCCESS, 'Logged In Scuccessfully!')
            return redirect(request.GET.get('next') or reverse('articles:home'))
        else:
            messages.add_message(request, messages.ERROR, 'Login Failed! Please check username and password')
            return render(request, 'accounts/login.html', { 'form' : AuthenticationForm(request) })
    return render(request, 'accounts/login.html', { 'form' :form })

def logout_view(request):
    if request.method == 'POST':    
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Logged Out Successfully!')
        return redirect(reverse('accounts:login'))
    return render(request, 'accounts/logout.html')

def register_view(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
            user_email = form.cleaned_data['email']
            messages.add_message(request, messages.SUCCESS, f'Verify Email! Email Sent To {user_email}')
            return redirect(reverse('accounts:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Please Check The Error Below')
    return render(request, 'accounts/register.html', { 'form': form })
