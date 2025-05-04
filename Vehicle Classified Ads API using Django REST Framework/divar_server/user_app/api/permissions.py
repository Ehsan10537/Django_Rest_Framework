from rest_framework import permissions




class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.id == view.kwargs.get('num'))


class IsUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.id == view.kwargs.get('num') or request.user.is_staff)
        