from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Creation d'un routeur
router = DefaultRouter()
router.register(r'users-list', UserViewSet)

# Inclure les routes
urlpatterns = [
    path('', include(router.urls)),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
