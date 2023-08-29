from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Project, Contributor, Issue, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'can_be_contacted', 'can_data_be_shared', 'age', 'consent']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError('Must be at least 15 years old to register.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class ContributorSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user_name']

class ProjectSerializer(serializers.ModelSerializer):
    creator = ContributorSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id','name', 'description', 'creator']

class IssueSerializer(serializers.ModelSerializer):
    # Champ pour sélectionner le contributeur auquel l'issue sera assignée
    creator = ContributorSerializer()
    class Meta:
        model = Issue
        fields = ['id','name', 'description', 'status', 'priority', 'tag', 'creator']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Utiliser read_only=True ici

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'created_time']
        read_only_fields = ['id', 'uuid', 'created_time']





