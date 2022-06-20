from django.contrib import admin
from photoload.models import User, Rate, Post, Comment

admin.site.register(User)
admin.site.register(Rate)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'title', 'author',]

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['id']
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
