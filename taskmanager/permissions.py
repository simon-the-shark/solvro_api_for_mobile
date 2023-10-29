from rest_framework import permissions


class IsOwnerOrReadOnlyProject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user
