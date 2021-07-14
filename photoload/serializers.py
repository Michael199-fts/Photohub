from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from photoload.models import User, Comment, Post

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegistrationSerializer, self).create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["name", "author", "photo"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "target", "target_comment", "author"]
