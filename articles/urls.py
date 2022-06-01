from django.urls import path

from .views import home_view, create_view

app_name = 'articles'

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_view, name='create'),
]