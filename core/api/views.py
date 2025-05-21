from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Task, Team, Notification, Comment
from .serializers import (
    TaskSerializer,
    TeamSerializer,
    NotificationSerializer,
    CommentSerializer,
    TaskDetailSerializer,
    TeamDetailSerializer
)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = LimitOffsetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['assigned_users']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve' and "comments" in self.request.path:
            return CommentSerializer
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer

    def get_queryset(self):
        if self.action == 'retrieve' and 'comments' in self.request.path:
            task_id = self.kwargs.get('id')
            return Comment.objects.filter(task_id=task_id)

        return Task.objects.all()


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        return queryset


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(task=self.kwargs.get('task_pk'))
        return queryset
