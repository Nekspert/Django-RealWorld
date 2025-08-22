from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import Article
from .models import Comment
from .serializers import CommentSerializer


class CRCommentView(APIView):
    def get(self, request: Request, slug: str, *args, **kwargs) -> Response:
        article = Article.objects.filter(slug=slug).exists()
        if not article:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(article__slug=slug)
        serializer = CommentSerializer(comments, many=True)
        return Response({'comments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request: Request, slug: str, *args, **kwargs) -> Response:
        comment = request.data.get('comment')
        if not comment:
            return Response({'errors': {'body': 'Comment data not found'}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=comment, context={'author': request.user.profile, 'article': article})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as ex:
            return Response({'errors': ex.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'comment': serializer.data}, status=status.HTTP_200_OK)


class DeleteCommentView(APIView):
    def delete(self, request: Request, slug: str, comment_id: int, *args, **kwargs) -> Response:
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return Response({'errors': {'body': 'Article not found'}}, status=status.HTTP_404_NOT_FOUND)

        try:
            article_comment = article.comments.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({'errors': {'body': 'Comment not found'}}, status=status.HTTP_404_NOT_FOUND)

        article_comment.delete()
        return Response(status=status.HTTP_200_OK)

