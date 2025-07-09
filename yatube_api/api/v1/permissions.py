from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать объект только автору,
    остальные пользователи имеют только права на чтение.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Наследник стандартного IsAuthenticated с кастомным сообщением об ошибке.
    """

    message = 'В доступе отказано.'
