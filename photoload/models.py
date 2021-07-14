from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    photo = models.ImageField(blank=True, verbose_name="Аватар")
    id_user = models.AutoField(primary_key=True, unique=True, verbose_name="ID пользователя")
    email = models.EmailField(verbose_name="E-mail", unique=True)


class Post(models.Model):
    photo = models.ImageField(verbose_name="Фото поста")
    name = models.CharField(max_length=30, verbose_name="Название")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор фото")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Время загрузки")


class Comment(models.Model):
    text = models.TextField(max_length=300, verbose_name="Текст комментария")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор комментария")
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    target_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name="Комментарий")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Время написания")


class Rate(models.Model):
    rate = models.SmallIntegerField(verbose_name="Оценка")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор оценки")
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
