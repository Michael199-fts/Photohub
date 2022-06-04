from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, F
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from photoload.paginator import CustomPagination
from photoload.serializers import PostSerializer, RegistrationSerializer, PersonalAccountSerializer,\
    CommentSerializer, RateSerializer, PostCommSerializer
from rest_framework.response import Response
from photoload.models import Post, User, Comment, Rate
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from photoload.services.posts_services.post_create_service import CreatePostService
from photoload.services.user_services.user_registration_service import RegistrationUserService


class PersonalAccountView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalAccountSerializer
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'personal_account.html'

    def get(self, request, pk):
        try:
            user_fields = User.objects.get(id_user=pk)
            serializer = self.serializer_class(user_fields)
            return Response({'account' : serializer.data})
        except ObjectDoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = User.objects.get(id_user=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Пользователь не найден", status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        service_result = RegistrationUserService.execute({**dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(RegistrationSerializer(service_result.result).data, status=status.HTTP_201_CREATED)


class PostGetView(ListAPIView):
    queryset = Post.objects.all
    serializer_class = PostCommSerializer

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("Пост не найден", status=status.HTTP_400_BAD_REQUEST)


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        service_result = CreatePostService.execute({'user':request.user.id, **dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(PostSerializer(service_result.result).data, status=status.HTTP_201_CREATED)



class PostUpdateDeleteView(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("Пост не найден", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = Post.objects.get(id=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Пост не найден", status=status.HTTP_400_BAD_REQUEST)


class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CursorPagination
    queryset = Comment.objects.all()

    def get(self, request, pk):
        try:
            posts = Comment.objects.filter(target=pk, target_comment=None)
            serializer = self.serializer_class(posts, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("Комментарий не найден", status=status.HTTP_400_BAD_REQUEST)



class NestedCommentView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CursorPagination
    queryset = Comment.objects.all()

    def get(self, request, pk):
        try:
            comments = Comment.objects.filter(target_comment=pk)
            serializer = self.serializer_class(comments, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("Комментарий не найден", status=status.HTTP_400_BAD_REQUEST)


class CreateCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

class UpdateDeleteCommentView(UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            serializer = self.serializer_class(comment)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("Комментарий не найден", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = Comment.objects.get(id=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Комментарий не найден", status=status.HTTP_400_BAD_REQUEST)


class RateView(CreateAPIView):
    serializer_class = RateSerializer
    queryset = Rate.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#{
#"username": "",
#"password": ""
#}
#https://api.vk.com/method/photos.getAlbums?user_ids=ave_satan199&access_token=a86e0d65de5dec8b895da78604ab80860a5b5d7c8bbce5757d223c76afa05d80d2b4e921030b932cb34b9&v=5.131