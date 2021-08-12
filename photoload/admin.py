from django.contrib import admin
from photoload.models import User, Rate, Post, Comment

admin.site.register(User)
admin.site.register(Rate)
admin.site.register(Comment)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'name', 'author',]
admin.site.register(Post, PostAdmin)
