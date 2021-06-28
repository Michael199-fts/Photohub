from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
from photoload.serializers import PostSerializer, UserSerializer
from rest_framework.response import Response
from photoload.models import Post, User


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserReg(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserChange(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class UserDelete(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostGet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostCreate(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostUpdate(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update(self, request, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class PostDelete(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
