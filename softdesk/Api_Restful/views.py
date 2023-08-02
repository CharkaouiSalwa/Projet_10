from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import Project, Contributor
from .serializers import ProjectSerializer
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # Seuls les utilisateurs authentifiés peuvent créer et lister les projets
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Enregistrez l'utilisateur actuel comme un nouvel objet Contributor
        contributor = Contributor.objects.create(user=self.request.user)
        # Enregistrez le projet en lui attribuant le contributeur et le créateur
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
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
