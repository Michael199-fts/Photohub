from django.urls import path
from photoload.views import PostList, PostCreateList

urlpatterns = [
    path('posts/', PostList.as_view()),
    path('create/', PostCreateList.as_view()),
]
