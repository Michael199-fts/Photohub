from django.urls import path
from photoload.views import PostList

urlpatterns = [
    path('posts/', PostList.as_view())
]
