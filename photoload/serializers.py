from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers
from photoload.models import User, Comment, Post, Rate


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'photo': {'use_url': True}
        }



class PostSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ["title", "author", "photo_url", "upload_date", "rating", "text"]

    def get_photo_url(self, obj):
        return 'http://127.0.0.1:8000/media/'+str(obj.photo)


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
