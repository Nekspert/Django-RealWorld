from django.urls import path

from . import views


urlpatterns = [
    path('tags', views.tags_list, name='tags_list'),
]
