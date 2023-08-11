from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import Project, Contributor, Issue
from .serializers import ProjectSerializer, IssueSerializer
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class IsProjectCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur est l'auteur du projet (peut modifier/supprimer)
        if request.method in permissions.SAFE_METHODS:
            return True  # Les utilisateurs peuvent effectuer des requêtes GET, HEAD, OPTIONS
        return obj.creator.user == request.user

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # Seuls les utilisateurs authentifiés peuvent créer et lister les projets
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Récupérer l'utilisateur actuel
        user = self.request.user
        # Créer un nouvel objet Contributor pour cet utilisateur (si nécessaire)
        contributor, _ = Contributor.objects.get_or_create(user=user)
        # Enregistrer le projet en lui attribuant le contributeur et le créateur
        serializer.save(creator=contributor)
        project = serializer.instance
        project.contributors.add(contributor)

    def post(self, request, *args, **kwargs):
        # Surchargez la méthode post pour renvoyer une réponse HTTP_201_CREATED avec les données du projet
        response = super().post(request, *args, **kwargs)
        response.status_code = HTTP_201_CREATED
        return response

class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectCreatorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

class IssueCreateView(CreateAPIView):
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        contributor = Contributor.objects.get(user=self.request.user)
        serializer.save(creator=contributor)


class IssueListView(ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
