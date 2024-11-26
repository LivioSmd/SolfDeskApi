from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',  # 'contributors', 'issue',
                    'type', 'date_created', 'date_updated', 'actif')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'role')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'description',
                    'assigned_user', 'project', 'priority',
                    'tag', 'status', 'date_created', 'date_updated')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'author', 'issue', 'date_created', 'date_updated')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
