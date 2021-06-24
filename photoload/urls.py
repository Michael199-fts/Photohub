from django.urls import path
from photoload.views import PostGet, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('get/post/', PostGet.as_view()),
    path('create/post/', PostCreate.as_view()),
    path('update/post/', PostUpdate.as_view()),
    path('delete/post/', PostDelete.as_view()),
]
