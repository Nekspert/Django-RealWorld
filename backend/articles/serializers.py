from rest_framework import serializers

from profiles.serializers import ProfileSerializer
from .models import Article
from .relations import TagRelatedField


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')

    slug = serializers.SlugField(read_only=True)
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(method_name='get_favorites_count')

    class Meta:
        model = Article
        fields = ('slug',
                  'title',
                  'description',
                  'body',
                  'tagList',
                  'createdAt',
                  'updatedAt',
                  'favorited',
                  'favoritesCount',
                  'author',)

    def create(self, validated_data: dict):
        author = self.context['request'].user.profile
        tags = validated_data.pop('tags', [])

        article = Article.objects.create(author=author, **validated_data)
        for tag in tags:
            article.tags.add(tag)

        return article

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get('request')

        if request is None:
            return False
        if not request.user.is_authenticated:
            return False

        return request.user.profile.has_favorited(instance)

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()
