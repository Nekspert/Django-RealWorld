from django.urls import path

from . import views


urlpatterns = [
    path('tags', views.TagView.as_view(), name='tags_list'),
]
