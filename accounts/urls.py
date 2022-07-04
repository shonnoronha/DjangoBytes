from django.urls import path
from .views import base_view, login_view, logout_view

app_name = 'accounts'

urlpatterns = [
    path('', base_view),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]