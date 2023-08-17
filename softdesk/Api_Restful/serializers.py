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
        fields = ['user', 'projects', 'issues', 'comments']

class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), required=False, many=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'project_type', 'contributors', 'creator')

class IssueSerializer(serializers.ModelSerializer):
    # Champ pour sélectionner le contributeur auquel l'issue sera assignée
    assignee = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), required=False)

    class Meta:
        model = Issue
        fields = ['id', 'project', 'status', 'priority', 'tag', 'creator', 'assignee', 'name', 'description']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'uuid', 'issue_link', 'description', 'issue', 'author', 'created_time']
        read_only_fields = ['id', 'uuid', 'created_time'] # on peut pas modifier ces champs








