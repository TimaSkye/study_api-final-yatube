from django.contrib import admin
from .models import Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админ-панель для модели Публикации."""
    list_display = ('id', 'text', 'pub_date', 'author', 'group', 'image',)
    search_fields = ('text', 'author__username',)
    list_filter = ('pub_date', 'group',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Админ-панель для модели Группы."""
    list_display = ('id', 'title', 'slug', 'description',)
    search_fields = ('title', 'description',)
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админ-панель для модели Комментарии."""
    list_display = ('id', 'text', 'created', 'author', 'post',)
    search_fields = ('text', 'author__username', 'post__text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админ-панель для модели Подписки."""
    list_display = ('id', 'user', 'following',)
    search_fields = ('user__username', 'following__username',)
    list_filter = ('user', 'following',)
