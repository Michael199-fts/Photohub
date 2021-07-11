from rest_framework import serializers
from photoload.models import User, Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password", "id_user", "photo"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["name", "author", "photo"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "target", "target_comment", "author"]
