from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
