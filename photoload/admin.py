from django.contrib import admin
from photoload.models import User
from photoload.models import Post
from photoload.models import Value_post
from photoload.models import Comment
from photoload.models import Value_comm
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Value_post)
admin.site.register(Comment)
admin.site.register(Value_comm)