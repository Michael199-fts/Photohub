from django.urls import path
from photoload.views import RegistrationAPIView, PersonalAccountView, CommentListView, NestedCommentView, \
    CreateCommentView, UpdateDeleteCommentView, PostRetrieveUpdateDestroyAPIView, PostCreateListAPIView, \
    RateCreateAPIView

urlpatterns = [
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='Посты'),
    path('post/', PostCreateListAPIView.as_view(), name='Посты'),
    path('registration/', RegistrationAPIView.as_view(), name='Регистрация'),
    path('personal_account/<int:pk>/', PersonalAccountView.as_view(), name='Личный кабинет'),
    path('comments/<int:pk>/', CommentListView.as_view(), name='Комментарии к посту'),
    path('nested_comments/<int:pk>/', NestedCommentView.as_view(), name='Вложенные комментарии'),
    path('create_commentary/', CreateCommentView.as_view(), name='Создание комментария'),
    path('commentary/<int:pk>/', UpdateDeleteCommentView.as_view(), name='Редактор комментария'),
    path('rate/<int:pk>/', RateCreateAPIView.as_view(), name='Оценка'),
]
