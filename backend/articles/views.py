from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.custompagination import LimitOffsetPaginationWithUpperBound
from .models import Article
from .serializers import ArticleSerializer


class GetOrCreateArticleView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        qs = Article.objects.all()

        tag = self.request.query_params.get('tag')
        author = self.request.query_params.get('author')
        favorited = request.query_params.get('favorited')

        if tag:
            qs = qs.filter(tags__tag=tag)
        if author:
            qs = qs.filter(author__user__username=author)
        if favorited:
            qs = qs.filter(favorited_by__user__username=favorited)

        qs = qs.distinct()
        total = qs.count()

        paginator = LimitOffsetPaginationWithUpperBound()
        page = paginator.paginate_queryset(qs, request, view=self)
        if page is None:
            serializer = ArticleSerializer(qs, many=True, context={'request': request})
            return Response({
                'count': total,
                'next': None,
                'previous': None,
                'results': {
                    'articles': serializer.data,
                    'articlesCount': total
                }
            }, status=status.HTTP_200_OK)

        serializer = ArticleSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response({'articles': serializer.data, 'articlesCount': total})

    def post(self, request: Request, *args, **kwargs) -> Response:
        article = request.data.get('article')
        if not article:
            return Response({'errors': {'body': 'article data now found'}}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleSerializer(data=article, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as ex:
            return Response({'errors': ex.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'article': serializer.data}, status=status.HTTP_201_CREATED)


class RUDArticleView(APIView):
    def get(self, request: Request, slug: str, *args, **kwargs) -> Response:
        article = Article.objects.filter(slug=slug).exists()
        if not article:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        article = Article.objects.get(slug=slug)
        serializer = ArticleSerializer(article, context={'request': request})

        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request: Request, slug: str, *args, **kwargs) -> Response:
        payload = request.data.get('article')
        if not payload:
            return Response({'errors': {'body': 'Article data not found'}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        if article.author.user != request.user:
            return Response({'errors': {'body': 'permission denied'}}, status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(article, data=payload, partial=True, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as ex:
            return Response({'errors': ex.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request: Request, slug: str) -> Response:
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        if request.user != article.author.user:
            return Response({'errors': {'body': 'permission denied'}}, status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response(status=status.HTTP_200_OK)


class ArticlesFavoriteView(APIView):
    def post(self, request: Request, slug: str, *args, **kwargs) -> Response:
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        cur_profile = request.user.profile
        cur_profile.favorite(article)
        serializer = ArticleSerializer(article)
        return Response({'article': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request: Request, slug: str, *args, **kwargs) -> Response:
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        cur_profile = request.user.profile
        cur_profile.unfavorite(article)
        serializer = ArticleSerializer(article)
        return Response({'article': serializer.data}, status=status.HTTP_200_OK)


class ArticleFeedView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(author__in=self.request.user.profile.follows.all())

    def list(self, request: Request, *args, **kwargs) -> Response:
        qs = self.get_queryset()
        total = qs.count()
        page = self.paginate_queryset(qs)

        serializer = ArticleSerializer(page, context={'request': request}, many=True)
        return self.get_paginated_response({'articles': serializer.data, 'articlesCount': total})
