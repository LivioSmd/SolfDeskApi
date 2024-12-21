from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

# Creating a router
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
# /projects/
# /projects/{pk}/

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'contributors', ContributorViewSet, basename='contributors')
project_router.register(r'issues', IssueViewSet, basename='issues')
# /projects/{project_pk}/contributors/
# /projects/{project_pk}/contributors/{pk}/
# /projects/{project_pk}/issues/{pk}/

issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
issue_router.register(r'comments', CommentViewSet, basename='comments')
# /projects/{project_pk}/issues/{pk}/comments
# /projects/{project_pk}/issues/{issue_pk}/comments/{pk}

# Inclure les routes
urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]
