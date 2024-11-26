from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from users.serializers import UserSerializer

from users.models import User


class ContributorDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Accepte un ID d'utilisateur

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role', 'project']


class ContributorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role']


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    project = serializers.StringRelatedField()  # renvoie seulement le __str__() / Sérialiser le projet (si nécessaire)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'project', 'issue', 'date_created', 'date_updated']


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'date_created']


class IssueDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'author', 'description',
            'assigned_user', 'project', 'comments', 'priority',
            'tag', 'status', 'date_created', 'date_updated'
        ]


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'priority', 'tag', 'status']


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'contributors', 'type', 'issues', 'date_created', 'date_updated',
                  'actif']


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type', 'date_created', 'date_updated', 'actif']
