from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from photoload.serializers import PostSerializer, RegistrationSerializer, PersonalAccountSerializer
from rest_framework.response import Response
from photoload.models import Post, User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class PersonalAccountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalAccountSerializer

    def get(self, request):
        user_fields = User.objects.get(username=request.user)
        serializer = self.serializer_class(user_fields)
        return Response(serializer.data)

    def put(self, request):
        instance = User.objects.get(username=request.user)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.update(instance, validated_data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        instance = User.objects.get(username=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED,)


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

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


class PostCreateView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED,)


class PostUpdateDelete(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = Post.objects.get(id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.update(instance, validated_data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = Post.objects.get(id=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#{
#"username": "",
#"password": ""
#}
