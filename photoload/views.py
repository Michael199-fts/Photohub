from rest_framework.generics import ListAPIView
from photoload.serializers import PostSerializer
from rest_framework.response import Response
from photoload.models import Post

class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
