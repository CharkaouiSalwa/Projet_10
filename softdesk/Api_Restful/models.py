from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField()
    consent = models.BooleanField()
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=False)

class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField('Api_Restful.Project', related_name='contributor_projects')
    issues = models.ManyToManyField('Api_Restful.Issue', related_name='contributor_issues')
    comments = models.ManyToManyField('Api_Restful.Comment', related_name='contributor_comments')

class Project(models.Model):
    name = models.CharField(max_length=100, default="name")
    description = models.TextField(default="description")

    BACKEND = 'backend'
    FRONTEND = 'frontend'
    IOS = 'ios'
    ANDROID = 'android'

    PROJECT_TYPES = [
        (BACKEND, 'Back-end'),
        (FRONTEND, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    ]
    project_type = models.CharField(max_length=10, choices=PROJECT_TYPES, default=BACKEND)
    contributors = models.ManyToManyField(Contributor, related_name='project_contributors')
    creator = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='created_projects')


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issue_projects')
    status = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    creator = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='created_issues')
    taches = models.CharField(max_length=100)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comment_issues')
    creator = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='created_comments')


