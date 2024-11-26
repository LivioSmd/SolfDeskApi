from django.db import models
from users.models import User


class Project(models.Model):
    BACKEND = 'BACKEND'
    FRONTEND = 'FRONTEND'
    IOS = 'IOS'
    ANDROID = 'ANDROID'
    # tuple de tuples, pour définir les choix
    TYPES_CHOICES = (
        (BACKEND, 'Back-end'),
        (FRONTEND, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android')
    )

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    type = models.CharField(max_length=12, choices=TYPES_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=255, default='Dev')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"


class Issue(models.Model):
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=5000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='author_issue')
    assigned_user = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='assigned_issue')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    )

    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'
    TAGS_CHOICES = (
        (BUG, 'Bug'),
        (FEATURE, 'Feature'),
        (TASK, 'Task')
    )

    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'
    STATUS_CHOICES = (
        (TODO, 'To-Do'),
        (IN_PROGRESS, 'InProgress'),
        (FINISHED, 'Finished')
    )

    priority = models.CharField(max_length=12, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=12, choices=TAGS_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=TODO)


class Comment(models.Model):
    description = models.CharField(max_length=5000)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='author_comment')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
