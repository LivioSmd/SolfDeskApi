from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorListSerializer, \
    ContributorDetailSerializer, IssueListSerializer, \
    IssueDetailSerializer, CommentListSerializer, CommentDetailSerializer
from users.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')  # Utilisez project_pk pour le nested router
        if project_pk:
            return Project.objects.filter(pk=project_pk)
        return Project.objects.all()  # Retourne tous les projets si project_id vide

    def perform_create(self, serializer):
        project = serializer.save()

        # Ajoutez l'utilisateur connecté comme contributeur avec le rôle 'Owner'
        Contributor.objects.create(user=self.request.user, project=project, role='Owner')


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')  # Utilisez project_pk pour le nested router
        contributor_pk = self.kwargs.get('pk')  # Utilisez project_pk pour le nested router
        if contributor_pk:
            return Contributor.objects.filter(project_id=project_pk, pk=contributor_pk)
        return Contributor.objects.filter(
            project_id=project_pk).all()  # Retourne tous les contributors si contributor_pk vide

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user_id = self.request.data.get('user')
        user = User.objects.get(id=user_id)

        # Vérifiez si cet utilisateur est déjà contributeur
        if Contributor.objects.filter(user=user, project=project).exists():
            raise Exception("This user is already a contributor for this project.")

        # Enregistrer le contributeur avec le rôle spécifié ou un rôle par défaut
        role = self.request.data.get('role', 'Dev')  # Si aucun rôle n'est spécifié, utiliser 'Dev'
        serializer.save(user=user, project=project, role=role)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')  # Utilisez project_pk pour le nested router
        issue_pk = self.kwargs.get('pk')  # Utilisez project_pk pour le nested router
        if issue_pk:
            return Issue.objects.filter(project_id=project_pk, pk=issue_pk)
        return Issue.objects.filter(project_id=project_pk).all()

    def perform_create(self, serializer):
        project_pk = self.kwargs.get('project_pk')  # Utilisez project_pk pour le nested router
        assigned_user = self.request.data.get('assigned_user')

        # Récupérer le contributeur auteur de l'issue
        author = Contributor.objects.get(user=self.request.user, project_id=project_pk)

        # Vérifier si un utilisateur assigné est spécifié
        if assigned_user:
            assigned_contributor = Contributor.objects.get(user_id=assigned_user, project_id=project_pk)
        else:
            # Si aucun utilisateur n'est assigné, l'auteur devient l'utilisateur assigné
            assigned_contributor = author

        # Sauvegarder l'instance
        serializer.save(
            project_id=project_pk,
            author=author,
            assigned_user=assigned_contributor
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')  # Utilisez project_pk pour le nested router
        issue_pk = self.kwargs.get('issue_pk')  # Utilisez project_pk pour le nested router
        comment_pk = self.kwargs.get('pk')  # Utilisez project_pk pour le nested router
        if comment_pk:
            return Comment.objects.filter(project_id=project_pk, issue_id=issue_pk, pk=comment_pk)
        return Comment.objects.filter(project_id=project_pk, issue_id=issue_pk).all()

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