from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers
from photoload.models import User, Comment, Post, Rate


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}



class PostSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    @staticmethod
    def get_rate(instance):
        rat = instance.targets.aggregate(rating=Sum('rate'))
        if not rat['rating']:
            return 0
        else:
            return rat['rating']
    class Meta:
        model = Post
        fields = ["name", "author", "photo", "upload_date", "rate",]


class CommentSerializer(serializers.ModelSerializer):
    flag = serializers.SerializerMethodField()

    @staticmethod
    def get_flag(instance):
        return instance.nested_comment.exists()

    class Meta:
        model = Comment
        fields = ['text', 'target', 'target_comment', 'author', 'flag', 'id',]



class PersonalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'photo', 'id_user',]
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate', 'author', 'target',]


class PostCommSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    @staticmethod
    def get_comment(instance):
        return CommentSerializer(instance.comment.filter(target_comment=None), many=True).data

    class Meta:
        model = Post
        fields = ["name", "author", "photo", "comment",]
