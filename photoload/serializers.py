from rest_framework import serializers
from photoload.models import User, Value_post, Value_comm, Comment, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "password", "id_user", "photo"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["raters", "sum_rate", "name", "author", "photo"]

class ValuePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value_post
        fields = ["rate", "author", "target"]

class ValueCommSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value_comm
        fields = ["rate", "author", "target"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "raters", "sum_rate", "target", "author"]