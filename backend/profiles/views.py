from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer


class ProfileView(APIView):
    def get(self, request: Request, username: str, *args, **kwargs) -> Response:
        other_user = get_user_model().objects.filter(username=username).exists()
        if not other_user:
            return Response({'errors': {'body': 'User does not exists'}}, status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.get(user__username=username)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request: Request, username: str, *args, **kwargs) -> Response:
        other_user = get_user_model().objects.filter(username=username).exists()
        if not other_user:
            return Response({'errors': {'body': 'User does not exists'}}, status=status.HTTP_404_NOT_FOUND)

        other_user = get_user_model().objects.get(username=username)
        cur_user = request.user
        if other_user.pk is cur_user.pk:
            return Response({'errors': {'body': 'You can not follow yourself.'}}, status=status.HTTP_400_BAD_REQUEST)

        cur_profile = cur_user.profile
        other_profile = other_user.profile
        # if cur_profile.is_following(other_profile):
        #     return Response()

        cur_profile.follow(other_profile)

        serializer = ProfileSerializer(instance=other_profile, context={'request': request})
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request: Request, username: str, *args, **kwargs) -> Response:
        other_user = get_user_model().objects.filter(username=username).exists()
        if not other_user:
            return Response({'errors': {'body': 'User does not exists'}}, status=status.HTTP_404_NOT_FOUND)

        other_user = get_user_model().objects.get(username=username)
        cur_user = request.user

        if other_user.pk is cur_user.pk:
            return Response({'errors': {'body': 'You can not unfollow yourself.'}}, status=status.HTTP_400_BAD_REQUEST)

        cur_profile = cur_user.profile
        cur_profile.unfollow(other_user.profile)

        serializer = ProfileSerializer(instance=other_user.profile, context={'request': request})
        return Response({'profile': serializer.data}, status=status.HTTP_200_OK)
