from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    photo = models.ImageField(blank=True, verbose_name="Аватар", upload_to='images/')
    email = models.EmailField(verbose_name="E-mail", unique=True)
    first_name = models.CharField(verbose_name="Имя", max_length=30)
    last_name = models.CharField(verbose_name="Фамилия", max_length=30)
    age = models.SmallIntegerField()


class Post(models.Model):
    photo = models.ImageField(verbose_name="Фото поста", upload_to='images/')
    title = models.CharField(max_length=30, verbose_name="Название")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор фото")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Время загрузки")
    text = models.TextField(max_length=1000)
    rating = models.IntegerField()


class Comment(models.Model):
    text = models.TextField(max_length=300, verbose_name="Текст комментария")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор комментария")
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост", related_name="comment")
    target_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name="Комментарий", related_name="nested_comment")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Время написания")


class Rate(models.Model):
    CHOICES = (
        (1, 'Плохо'),
        (2, 'Нормально'),
        (3, 'Хорошо'),
        (4, 'Легендарно'),
    )
    rate = models.SmallIntegerField(choices=CHOICES, default='2')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор оценки")
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост",
                               related_name="targets", related_query_name="target")
