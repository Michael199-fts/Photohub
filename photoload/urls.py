from django.urls import path
from photoload.views import PostCreateUpdateGet, LoginAPIView, RegistrationAPIView

urlpatterns = [
    path('post/', PostCreateUpdateGet.as_view()),
    path('auth/', LoginAPIView.as_view()),
    path('reg/', RegistrationAPIView.as_view()),
]
