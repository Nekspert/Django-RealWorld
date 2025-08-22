from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        read_only_fields = ('tag',)

    def to_representation(self, instance) -> str:
        return instance.tag
