from django.urls import path

from . import views

urlpatterns = [
    path('', views.convert, name='convert'),
    path('old', views.convert_old, name='convert_old'),
]