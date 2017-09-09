from rest_framework import permissions


class UserIsNoteOwnerOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def check_object_permission(self, user, obj):
        return (user and user.is_authenticated() and
          (user.is_staff or obj.owner == user))

    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request.user, obj)
