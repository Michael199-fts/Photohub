from django.urls import path
from photoload.views import PostGet, PostCreate, PostUpdate, PostDelete, UserReg, UserList, UserChange, UserDelete

urlpatterns = [
    path('get/post/', PostGet.as_view()),
    path('create/post/', PostCreate.as_view()),
    path('update/post/', PostUpdate.as_view()),
    path('delete/post/', PostDelete.as_view()),
    path('reg/', UserReg.as_view()),
    path('home/', UserList.as_view()),
    path('settings/', UserChange.as_view()),
    path('del_user', UserDelete.as_view()),
]
