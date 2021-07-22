from django.contrib import admin
from photoload.models import User, Rate, Post, Comment

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Rate)
admin.site.register(Comment)
