from django.urls import path

from . import views


urlpatterns = [
    path('articles/<slug:slug>/comments', views.CRCommentView.as_view(), name='create_read_comment'),
    path('articles/<slug:slug>/comments/<int:comment_id>', views.DeleteCommentView.as_view(), name='delete_comment'),
]