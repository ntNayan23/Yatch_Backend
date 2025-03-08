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

class IsAdminUserWithRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff and
            request.user.role == 'admin'
        )
        
class IsCaptain(BasePermission):
    """
    Allows access only to admin users
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'captain'
        )

class IsApprovedVendor(BasePermission):
    message = "Your vendor account is pending approval"

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'vendor' and
            request.user.vendor_profile.approval_status == 'approved'
        )
        
class IsActiveUser(BasePermission):
    """Check if user has activated their account"""
    def has_permission(self, request, view):
        return request.user.is_active