from django.urls import path

from . import views


urlpatterns = [
    path('articles', views.GetOrCreateArticleView.as_view(), name='articles_list'),
    path('articles/feed', views.ArticleFeedView.as_view(), name='article_feed'),
    path('articles/<slug:slug>', views.RUDArticleView.as_view(), name='article'),
    path('articles/<slug:slug>/favorite', views.ArticlesFavoriteView.as_view(), name='favorite_article'),
]
