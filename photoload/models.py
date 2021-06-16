from django.db import models
import datetime

class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=50)
    photo = models.ImageField(blank=True)
    id_user = models.AutoField(primary_key = True, unique=True)

class Post(models.Model):
    photo = models.ImageField()
    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    raters = models.IntegerField(default=0)
    sum_rating = models.IntegerField(default=0)
    upload_date = models.DateTimeField(default=datetime.datetime.now())

class Comment(models.Model):
    text = models.TextField(max_length=300)
    sum_rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=datetime.datetime.now())

class Value(models.Model):
    rate = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    target_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    target_com = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True)