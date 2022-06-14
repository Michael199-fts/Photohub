from django.urls import path
from photoload.views import RegistrationAPIView, PostRetrieveUpdateDestroyAPIView, PostCreateListAPIView, \
    RateCreateAPIView, CommentCreateListAPIView, CommentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('post/', PostCreateListAPIView.as_view()),
    path('registration/', RegistrationAPIView.as_view()),
    path('comment/', CommentCreateListAPIView.as_view()),
    path('comment/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('rate/<int:pk>/', RateCreateAPIView.as_view()),
]
