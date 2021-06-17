from django.db import models
import datetime

class User(models.Model):
    name = models.CharField(max_length=40, verbose_name="Имя пользователя")
    email = models.EmailField(blank=True, verbose_name="E-mail пользователя")
    password = models.CharField(max_length=50, verbose_name="Пароль")
    photo = models.ImageField(blank=True, verbose_name="Аватар")
    id_user = models.AutoField(primary_key = True, unique=True, verbose_name="ID пользователя")

class Post(models.Model):
    photo = models.ImageField(verbose_name="Фото поста")
    raters = models.SmallIntegerField(default=0, verbose_name="Число оценщиков")
    sum_rate = models.SmallIntegerField(default=0, verbose_name="Сумма оценок")
    name = models.CharField(max_length=30, verbose_name="Название")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор фото")
    upload_date = models.DateTimeField(verbose_name="Время загрузки")

class Comment(models.Model):
    text = models.TextField(max_length=300, verbose_name="Текст комментария")
    raters = models.SmallIntegerField(default=0, verbose_name="Число оценщиков")
    sum_rate = models.SmallIntegerField(default=0, verbose_name="Сумма оценок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    target = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name="Пост")
    upload_date = models.DateTimeField(verbose_name="Время написания")

class Value_post(models.Model):
    rate = models.SmallIntegerField(verbose_name="Оценка")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор оценки")
    target = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name="Пост")

class Value_comm(models.Model):
    rate = models.SmallIntegerField(verbose_name="Оценка")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор оценки")
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Комментарий")