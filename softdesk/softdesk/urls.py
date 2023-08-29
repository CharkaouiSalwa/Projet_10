from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Api_Restful.views import UserRegisterView, UserLoginView, ProjectListCreateView, \
    ProjectRetrieveUpdateDestroyView, IssueListCreateView, \
    CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update-destroy'),
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
   # path('issues/', IssueListCreateView.as_view(), name='issue-list-create-filtered'),  # Nouveau chemin avec filtres
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create-filtered'),  # Nouveau chemin avec filtres
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),
]
