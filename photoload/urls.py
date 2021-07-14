from django.urls import path
from photoload.views import PostCreateUpdate, RegistrationAPIView, AuthTokenView

urlpatterns = [
    path('post/', PostCreateUpdate.as_view()),
    path('reg/', RegistrationAPIView.as_view()),
    path('auth/', AuthTokenView.as_view()),
]
