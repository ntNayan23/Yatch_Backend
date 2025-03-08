from .profile_views import (
    CustomerRegistrationView,
    VendorRegistrationView,
    LoginView,
    SuperUserRegistrationView,
    VendorProfileCompletionView,
    AccountActivationView,
)

from .dashboard_views import (
    CustomerDashboardView,
    VendorDashboardView,
    CaptainDashboardView
)

__all__ = [
    'CustomerRegistrationView',
    'VendorRegistrationView',
    'LoginView',
    'CustomerDashboardView',
    'VendorDashboardView',
    'CaptainDashboardView',
    'SuperUserRegistrationView',
    'VendorProfileCompletionView',
    'AccountActivationView'
]