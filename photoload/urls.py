from django.urls import path
from photoload.views import PostCreateUpdateGet

urlpatterns = [
    path('post/', PostCreateUpdateGet.as_view()),
]
