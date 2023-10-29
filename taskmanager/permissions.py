from rest_framework import permissions


class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user


class IsPartOfThisProject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the task
        return (obj.created_by == request.user) or (request.user in obj.project.other_users.all())
