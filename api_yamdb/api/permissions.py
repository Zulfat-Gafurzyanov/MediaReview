from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        pass
        # # У администратора полный доступ.
        # if request.user.is_admin:
        #   return True
        # # У пользователей только GET-запрос.
        # return (request.method in permissions.SAFE_METHODS)
