from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Project, Contributor, Issue, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'can_be_contacted', 'can_data_be_shared', 'age', 'consent']

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
    class Meta:
        model = Contributor
        fields = ['user', 'projects', 'issues', 'comments']  # Remplacez __all__ par la liste des champs souhaités

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['contributors', 'creator']

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['project', 'status', 'priority', 'creator', 'taches']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['issue', 'creator']










