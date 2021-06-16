from django.contrib import admin
from photoload.models import User
from photoload.models import Post
from photoload.models import Value
from photoload.models import Comment
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Value)
admin.site.register(Comment)