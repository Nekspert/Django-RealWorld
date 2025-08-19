from django.urls import path

from . import views


urlpatterns = [
    path('profiles/<slug:username>', views.ProfileView.as_view(), name='current_user'),
    path('profiles/<slug:username>/follow', views.ProfileView.as_view(), name='follow_user'),
    path('profiles/<slug:username>/follow', views.ProfileView.as_view(), name='delete_user'),
]
