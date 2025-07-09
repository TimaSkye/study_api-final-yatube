from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly
from posts.models import Post, Group
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр сообществ (только чтение)."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]  # Доступно всем


class PostViewSet(viewsets.ModelViewSet):
    """CRUD публикаций с пагинацией и правами доступа."""
    queryset = Post.objects.select_related('author', 'group').all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD комментариев, связанных с конкретным постом."""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def _get_post(self):
        """
        Вспомогательный метод для получения объекта Post по post_id из URL.
        """
        return get_object_or_404(
            Post.objects.select_related('author', 'group'),
            pk=self.kwargs.get('post_id')
        )

    def get_queryset(self):
        post = self._get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self._get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет для подписок с поддержкой только GET (list) и POST (create).
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        if serializer.validated_data.get('following') == self.request.user:
            raise ValidationError("Нельзя подписаться на самого себя.")
        serializer.save(user=self.request.user)
