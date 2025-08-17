from django.urls import path

from . import views


urlpatterns = [
    path('user', views.current_user, name='current_user'),
]
