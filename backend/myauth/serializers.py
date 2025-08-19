from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import serializers

from profiles.serializers import ProfileSerializer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True, max_length=254, style={'input_type': 'email'})
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password',)

    def create(self, validated_data: dict):
        password = validated_data.pop('password')
        try:
            with transaction.atomic():
                user = get_user_model().objects.create_user(password=password, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                    {'errors': {'message': 'User with this email or username already exists'}})
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], required=False)
    profile = ProfileSerializer(required=False, write_only=True)

    bio = serializers.CharField(source='profile.bio', required=False, allow_blank=True, allow_null=True)
    image = serializers.CharField(source='profile.image', required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'bio', 'image', 'password', 'profile')

    def update(self, instance, validated_data: dict):
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()

        return instance
