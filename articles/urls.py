from django.urls import path

from .views import home_view, create_view, detail_view

app_name = 'articles'

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_view, name='create'),
    path('detail/<int:id>/', detail_view, name='detail'),
]