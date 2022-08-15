from django.urls import path
from .views import base_view, login_view, logout_view, register_view, activate_user, request_verification

app_name = 'accounts'

urlpatterns = [
    path('', base_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('activate/<uidb64>/<token>', activate_user, name='activate'),
    path('request-verification/', request_verification, name='request-verification')
]