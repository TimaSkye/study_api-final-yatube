from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly, IsAuthenticated
from posts.models import Post, Group, Follow
from .serializers import (PostSerializer, GroupSerializer,
                          CommentSerializer, FollowSerializer
                          )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр сообществ (только чтение)."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """CRUD публикаций с пагинацией и правами доступа."""
    queryset = Post.objects.select_related('author', 'group').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD комментариев, связанных с конкретным постом."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    # Flake8 не пропустил моржовый оператор =((
    def get_queryset(self):
        post = get_object_or_404(
            Post.objects.select_related('author', 'group'),
            pk=self.kwargs.get('post_id')
        )
        return post.comments.all()

    # И здесь тоже =((
    def perform_create(self, serializer):
        post = get_object_or_404(
            Post.objects.select_related('author', 'group'),
            pk=self.kwargs.get('post_id')
        )
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """CRUD подписок с поиском и ограничением по текущему пользователю."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
