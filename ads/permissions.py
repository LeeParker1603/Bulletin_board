from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    Разрешает изменение и удаление объекта только его автору
    или пользователю с ролью admin.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.author == request.user or request.user.is_admin
