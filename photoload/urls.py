from django.urls import path
from photoload.views import RegistrationAPIView, PostRetrieveUpdateDestroyAPIView, PostCreateListAPIView, \
    RateCreateAPIView, CommentCreateListAPIView, CommentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('post/', PostCreateListAPIView.as_view()),
    path('registration/', RegistrationAPIView.as_view()),
    path('post/<int:pk>/comments/', CommentCreateListAPIView.as_view()),
    path('post/<int:post>/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('post/<int:pk>/rate/', RateCreateAPIView.as_view()),
]
