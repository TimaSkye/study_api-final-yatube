from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group (сообщество)."""

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post (публикация)."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment (комментарий)."""
    author = SlugRelatedField(slug_field='username', read_only=True)
    post = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow (подписка)."""
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Подписка уже существует.'
            )
        ]

    def validate(self, data):
        following = get_object_or_404(User, username=data['following'])
        if self.context['request'].user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.')
        return data
