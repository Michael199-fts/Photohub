from django.urls import path
from photoload.views import PostUpdateDelete, RegistrationAPIView, AuthTokenView, PersonalAccountView,\
    PostListView, PostCreateView

urlpatterns = [
    path('post/<int:pk>', PostUpdateDelete.as_view(), name='Редактор постов'),
    path('c_post/', PostCreateView.as_view(), name='Создание поста'),
    path('reg/', RegistrationAPIView.as_view(), name='Регистрация'),
    path('auth/', AuthTokenView.as_view(), name='Аутентификация'),
    path('pa/<int:pk>', PersonalAccountView.as_view(), name='Личный кабинет'),
    path('posts/', PostListView.as_view(), name='Лист постов'),
]
