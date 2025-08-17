from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import serializers


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
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'bio', 'image',)


