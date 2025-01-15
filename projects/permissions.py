from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import Contributor, Issue, Comment


class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Access for authenticated administrator users only
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class ProjectPermission(BasePermission):
    """ Permission to allow access only to contributors to a project """

    def has_permission(self, request, view):  # ou has_object_permission
        # Retrieves project id from URL parameters
        project_id = view.kwargs.get('pk')

        if request.method not in permissions.SAFE_METHODS:  # safe methods = GET, HEAD or OPTIONS.
            # If the contributor makes a request other than GET
            if project_id:
                # Returns a boolean depending on whether the contributor is the project owner or not.
                return Contributor.objects.filter(user=request.user, project_id=project_id, role='Owner').exists()
            else:  # POST case
                return True
        elif project_id and request.method in permissions.SAFE_METHODS:
            # If the contributor makes a GET request + he's part of the project
            return Contributor.objects.filter(user=request.user, project_id=project_id).exists()
        elif not project_id:
            # Case to display all projects
            return True
        else:
            return False


class InsideProjectPermission(BasePermission):
    """ Permission for Contributors & Issues & Comments """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        issue_id = ''
        comment_id = ''

        contributor = Contributor.objects.get(user=request.user, project_id=project_id)
        isContributor = Contributor.objects.filter(user=request.user, project_id=project_id).exists()

        # Assigns values correctly, as they change depending on the request url
        if view.kwargs.get('issue_pk'):
            issue_id = view.kwargs.get('issue_pk')
            if view.kwargs.get('pk'):
                comment_id = view.kwargs.get('pk')
        elif view.kwargs.get('pk'):
            issue_id = view.kwargs.get('pk')

        if (isContributor and request.method in permissions.SAFE_METHODS
                or isContributor and request.method == 'POST'):
            # Case where the contributor makes a GET / POST request (to create) + he's part of the project
            return True
        elif isContributor not in permissions.SAFE_METHODS:
            # If the contributor makes a request other than GET
            if comment_id:  # the case if it's just a comment
                # Checks if it's the author of the comment and return True if so
                comment = Comment.objects.get(project_id=project_id, pk=comment_id)
                return contributor == comment.author
            elif issue_id:   # the case if it's just an issue
                # Checks if it's the author of the issue and return True if so
                issue = Issue.objects.get(project_id=project_id, pk=issue_id)
                return contributor == issue.author
        else:
            return False
