from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#définir la pérmission
class IsProjectCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'auteur du projet (peut modifier/supprimer)
        if request.method in permissions.SAFE_METHODS:
            return True  # Les utilisateurs peuvent effectuer des requêtes GET, HEAD, OPTIONS
        return obj.creator.user == request.user
#class Project
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # Seuls les utilisateurs authentifiés peuvent créer et lister les projets
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        # Récupérer l'utilisateur actuel
        user = self.request.user
        # Créer un nouvel objet Contributor pour cet utilisateur (si nécessaire)
        contributor, _ = Contributor.objects.get_or_create(user=user)
        # Enregistrer le projet en lui attribuant le contributeur et le créateur
        serializer.save(creator=contributor)
        project = serializer.instance
        project.contributors.add(contributor)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectCreatorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

#class Issue
class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        id_project = self.request.query_params.get('id_project')
        if not id_project:
            return Issue.objects.none()
        return Issue.objects.filter(project_id=id_project)

    def perform_create(self, serializer):
        contributor = Contributor.objects.get(user=self.request.user)
        serializer.save(creator=contributor)

#class Comment

class CommentListCreateView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        id_issue = self.request.query_params.get('id_issue')
        if not id_issue:
            return Comment.objects.none()
        return Comment.objects.filter(issue_id=id_issue)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        comment = serializer.instance
        if self.request.user == comment.author:
            serializer.save()
        else:
            raise PermissionDenied("Vous n'avez pas la permission de mettre à jour cette ressource.")

    def perform_destroy(self, instance):
        if self.request.user == instance.author:
            instance.delete()
        else:
            raise PermissionDenied("Vous n'avez pas la permission de supprimer cette ressource.")
