from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from photoload.serializers import PostSerializer, RegistrationSerializer, CommentSerializer
from rest_framework.response import Response

from photoload.services.comment_services.comment_create_service import CreateCommentService
from photoload.services.comment_services.comment_delete_service import DeleteCommentService
from photoload.services.comment_services.comment_list_service import GetCommentListService
from photoload.services.comment_services.comment_patch_service import UpdateCommentService
from photoload.services.comment_services.comment_retrieve_service import GetCommentService
from photoload.services.posts_services.post_create_service import CreatePostService
from photoload.services.posts_services.post_delete_service import DeletePostService
from photoload.services.posts_services.post_list_service import GetPostListService
from photoload.services.posts_services.post_patch_service import UpdatePostService
from photoload.services.posts_services.post_retrieve_service import GetPostService
from photoload.services.rate_services.rate_create_service import CreateRateService
from photoload.services.user_services.user_registration_service import RegistrationUserService


class RegistrationAPIView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        service_result = RegistrationUserService.execute({**dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(RegistrationSerializer(service_result.result).data, status=status.HTTP_201_CREATED)


class PostCreateListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        service_result = GetPostListService.execute({'sort_by':request.query_params.get('sort_by'),
                                                     'filter_by':request.query_params.get('filter_by'),
                                                     'filter_value':request.query_params.get('filter_value')})
        return Response(PostSerializer(service_result.result, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        service_result = CreatePostService.execute({'user_id':request.user.id,
                                                    **dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(PostSerializer(service_result.result).data, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        service_result = GetPostService.execute({'pk':kwargs.get('pk')})
        return Response(PostSerializer(service_result.result).data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        service_result = UpdatePostService.execute({'pk':kwargs.get('pk'), 'user_id':request.user.id,
                                                    **dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(PostSerializer(service_result.result).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        service_result = DeletePostService.execute({'pk':kwargs.get('pk'), 'user_id':request.user.id,
                                                    **dict(request.data.items())})
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RateCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        service_result = CreateRateService.execute({'post_id':kwargs.get('pk'), 'user_id': request.user.id,
                                                    **dict(request.data.items())})
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response("Оценка отправлена", status=status.HTTP_201_CREATED)


class CommentCreateListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        service_result = GetCommentListService.execute({'pk':kwargs.get('pk'),
                                                    'sort_by':request.query_params.get('sort_by'),
                                                     'filter_by':request.query_params.get('filter_by'),
                                                     'filter_value':request.query_params.get('filter_value'),
                                                    'nested_flag':request.query_params.get('nested_flag')})
        return Response(CommentSerializer(service_result.result, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        service_result = CreateCommentService.execute({'post_id':kwargs.get('pk'), 'user_id':request.user.id,
                                                       **dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(CommentSerializer(service_result.result).data, status=status.HTTP_201_CREATED)


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        service_result = GetCommentService.execute({'pk':kwargs.get('pk')})
        return Response(CommentSerializer(service_result.result).data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        service_result = UpdateCommentService.execute({'pk':kwargs.get('pk'), 'user_id':request.user.id,
                                                       **dict(request.data.items())}, request.FILES.dict())
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(CommentSerializer(service_result.result).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        service_result = DeleteCommentService.execute({'pk':kwargs.get('pk'), 'user_id':request.user.id,
                                                       **dict(request.data.items())})
        if bool(service_result.error_report):
            return Response(service_result.error_report, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
