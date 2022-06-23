from django.urls import path

from .views import (
    home_view,
    create_view,
    detail_view,
    hx_detail_view
)

app_name = 'articles'

urlpatterns = [
    path('', home_view, name='home'),
    path('create/', create_view, name='create'),
    path('detail/<slug:slug>/', detail_view, name='detail'),
    path('hx/detail/<slug:slug>/', hx_detail_view, name='hx-detail'),
]