from django.urls import path
from photoload.views import PostCreateUpdateGet, LoginAPIView, RegistrationAPIView

urlpatterns = [
    path('post/', PostCreateUpdateGet.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('auth/', RegistrationAPIView.as_view()),
]
