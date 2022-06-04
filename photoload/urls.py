from django.urls import path
from photoload.views import PostUpdateDeleteView, RegistrationAPIView, PersonalAccountView, \
    PostCreateView, CommentListView, NestedCommentView, CreateCommentView, UpdateDeleteCommentView, \
    PostGetView, RateView

urlpatterns = [
    path('posts/<int:pk>', PostUpdateDeleteView.as_view(), name='Редактор постов'),
    path('create_post/', PostCreateView.as_view(), name='Создание поста'),
    path('registration/', RegistrationAPIView.as_view(), name='Регистрация'),
    path('personal_account/<int:pk>', PersonalAccountView.as_view(), name='Личный кабинет'),
    path('comments/<int:pk>', CommentListView.as_view(), name='Комментарии к посту'),
    path('nested_comments/<int:pk>', NestedCommentView.as_view(), name='Вложенные комментарии'),
    path('create_commentary/', CreateCommentView.as_view(), name='Создание комментария'),
    path('commentary/<int:pk>', UpdateDeleteCommentView.as_view(), name='Редактор комментария'),
    path('post_with_commentary/<int:pk>', PostGetView.as_view(), name='Просмотр поста'),
    path('rate/', RateView.as_view(), name='Оценка'),
]
