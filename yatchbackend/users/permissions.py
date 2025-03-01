from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """
    Allows access only to customers
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'customer'
        )

class IsVendor(BasePermission):
    """
    Allows access only to vendors
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'vendor'
        )

class IsAdmin(BasePermission):
    """
    Allows access only to admin users
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )

class IsApprovedVendor(IsVendor):
    """
    Allows access only to approved vendors
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
               request.user.vendor_profile.is_approved