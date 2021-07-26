from django.urls import path
from photoload.views import PostUpdateDeleteView, RegistrationAPIView, AuthTokenView, PersonalAccountView, \
    PostListView, PostCreateView, CommentListView, NestedCommentView, CreateCommentView, UpdateDeleteCommentView

urlpatterns = [
    path('post/<int:pk>', PostUpdateDeleteView.as_view(), name='Редактор постов'),
    path('c_post/', PostCreateView.as_view(), name='Создание поста'),
    path('reg/', RegistrationAPIView.as_view(), name='Регистрация'),
    path('auth/', AuthTokenView.as_view(), name='Аутентификация'),
    path('pa/<int:pk>', PersonalAccountView.as_view(), name='Личный кабинет'),
    path('posts/', PostListView.as_view(), name='Лист постов'),
    path('comments/<int:pk>', CommentListView.as_view(), name='Комментарии к посту'),
    path('nested_comments/<int:pk>', NestedCommentView.as_view(), name='Вложенные комментарии'),
    path('c_comment/', CreateCommentView.as_view(), name='Создание комментария'),
    path('comment/<int:pk>', UpdateDeleteCommentView.as_view(), name='Редактор комментария'),
]
