from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только администраторам изменять данные.
    Остальные пользователи могут только читать данные.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAdminByRole(permissions.BasePermission):
    """Разрешение, предоставляющее доступ только администраторам."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, предоставляющее полные права доступа
    авторам, администраторам и модераторам.
    Остальные пользователи могут только читать данные.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.author == request.user or request.user.is_admin
                or request.user.is_moderator)
        )
