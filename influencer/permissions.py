from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission allowing unauthenticated or regular users read-only (GET, HEAD, OPTIONS) access,
    while restricting creation, modification, and deletion to admin/staff members.
    """

    def has_permission(self, request, view):
        # Allow read-only operations for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Require staff/admin privileges for write operations (POST, PUT, PATCH, DELETE)
        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission allowing access only to the owner of an object or staff members.
    Assumes the model has a `user` attribute or is the `User` model itself.
    """

    def has_permission(self, request, view):
        # Must be authenticated to evaluate object ownership
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Admin / staff members have full access
        if request.user.is_staff:
            return True

        # Check if the object is the User model instance itself
        if obj == request.user:
            return True

        # Check if the object belongs to the request user (e.g., obj.user)
        return getattr(obj, 'user', None) == request.user