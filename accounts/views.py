from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import SignInForm
from .utils import generate_token

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }
    email_body = render_to_string('accounts/activate.html', context)

    email = EmailMessage(subject=email_subject,body=email_body,from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()

def base_view(request):
    return redirect(reverse('articles:home'))

def login_view(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
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
            username = form.cleaned_data['username']
            user = get_object_or_404(User, username=username)
            send_activation_email(user, request)
            user_email = form.cleaned_data['email']
            messages.add_message(request, messages.SUCCESS, f'Verify Email! Email Sent To {user_email}')
            return redirect(reverse('accounts:login'))
        else:
            messages.add_message(request, messages.ERROR, 'Please Check The Error Below')
    return render(request, 'accounts/register.html', { 'form': form })

def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    
    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your Email Was Successfully Verified!You can Login Now!!!')
        return redirect(reverse('accounts:login'))
    
    messages.add_message(request, messages.ERROR, 'Oops Something Went Wrong!!!')
    return redirect(reverse('accounts:login'))

@login_required
def request_verification(request):
    user = request.user
    if request.POST and (not user.is_email_verified):
        send_activation_email(user, request)
        messages.add_message(request, messages.SUCCESS, f'Email Successfully sent to {user.email}')
        return redirect(reverse('accounts:home'))
    return render(request, 'accounts/request-verification.html')
