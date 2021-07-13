import jwt
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')
        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({'id':self.pk,'exp':str(dt.strftime('%S'))}, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


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
