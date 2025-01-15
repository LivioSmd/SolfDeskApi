from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project, Contributor, Issue, Comment
from .permissions import ProjectPermission, InsideProjectPermission
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, \
    ContributorDetailSerializer, IssueListSerializer, \
    IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer
from users.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ProjectPermission]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')  # Use project_pk for the nested router
        if project_pk:
            return Project.objects.filter(pk=project_pk)
        return Project.objects.all()  # Returns all projects if project_id is empty

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = serializer.save()

        # Add the logged-in user as a contributor with the 'Owner' role
        Contributor.objects.create(user=self.request.user, project=project, role='Owner')


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, InsideProjectPermission]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        contributor_pk = self.kwargs.get('pk')
        if contributor_pk:
            return Contributor.objects.filter(project_id=project_pk, pk=contributor_pk)
        return Contributor.objects.filter(project_id=project_pk).all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user_id = self.request.data.get('user')
        user = User.objects.get(id=user_id)

        # Check if this user is already a contributor
        if Contributor.objects.filter(user=user, project=project).exists():
            raise Exception("This user is already a contributor for this project.")

        # Register the contributor with the specified role or a default role
        role = self.request.data.get('role', 'Dev')  # If no role is specified, use 'Dev'.
        serializer.save(user=user, project=project, role=role)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, InsideProjectPermission]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('pk')
        if issue_pk:
            return Issue.objects.filter(project_id=project_pk, pk=issue_pk)
        return Issue.objects.filter(project_id=project_pk).all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        project_pk = self.kwargs.get('project_pk')
        assigned_user = self.request.data.get('assigned_user')

        # Retrieve the contributor who created the issue
        author = Contributor.objects.get(user=self.request.user, project_id=project_pk)

        # Check if an assigned user is specified
        if assigned_user:
            assigned_contributor = Contributor.objects.get(user_id=assigned_user, project_id=project_pk)
        else:
            # If no user is assigned, the author becomes the assigned user
            assigned_contributor = author

        # Save instance
        serializer.save(
            project_id=project_pk,
            author=author,
            assigned_user=assigned_contributor
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, InsideProjectPermission]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        comment_pk = self.kwargs.get('pk')
        if comment_pk:
            return Comment.objects.filter(project_id=project_pk, issue_id=issue_pk, pk=comment_pk)
        return Comment.objects.filter(project_id=project_pk, issue_id=issue_pk).all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs.get('issue_pk'))
        project = Project.objects.get(id=self.kwargs.get('project_pk'))
        description = self.request.data.get('description')
        author = Contributor.objects.get(user=self.request.user, project=project)

        serializer.save(
            project=project,
            issue=issue,
            author=author,
            description=description
        )
