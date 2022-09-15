from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return any([
                request.user.is_admin,
                request.user.is_superuser
            ])

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return any([
                request.user.is_admin,
                request.user.is_superuser
            ])


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user))


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin)
                or (request.user.is_authenticated
                    and request.user.is_user)
                or (request.user.is_authenticated
                    and request.user.is_moderator))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user)
                or (request.user.is_admin)
                or (request.user.is_moderator))
