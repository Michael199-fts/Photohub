from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from photoload.serializers import PostSerializer, RegistrationSerializer, LoginSerializer
from rest_framework.response import Response
from photoload.models import Post


class PostCreateUpdateGet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request):
        instance = self.get_object()
        serializer = PostSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'token': serializer.data.get('token', None),},status=status.HTTP_201_CREATED,)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
