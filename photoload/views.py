from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from photoload.paginator import CustomPagination
from photoload.serializers import PostSerializer, RegistrationSerializer, PersonalAccountSerializer
from rest_framework.response import Response
from photoload.models import Post, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class PersonalAccountView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalAccountSerializer
    queryset = User.objects.all()

    def get(self, request, pk):
        user_fields = User.objects.get(id_user=pk)
        serializer = self.serializer_class(user_fields)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            instance = User.objects.get(id=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Пост не найден", status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AuthTokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class PostListView(APIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


class PostUpdateDelete(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            instance = Post.objects.get(id=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Пост не найден", status=status.HTTP_400_BAD_REQUEST)



#{
#"username": "",
#"password": ""
#}
