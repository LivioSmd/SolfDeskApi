from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Creation d'un routeur
router = DefaultRouter()
router.register(r'users', UserViewSet)

# Inclure les routes
urlpatterns = [
    path('', include(router.urls)),
]
