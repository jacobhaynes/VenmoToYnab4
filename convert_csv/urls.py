from django.urls import path

from . import views

urlpatterns = [
    path('', views.convert, name='convert'),
]