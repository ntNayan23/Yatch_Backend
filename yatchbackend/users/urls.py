from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomerRegistrationView,
    VendorRegistrationView,
    LoginView,
    CustomerDashboardView,
    VendorDashboardView,
    CaptainDashboardView,
    SuperUserRegistrationView,
    VendorProfileCompletionView,
    AccountActivationView,
    
)
urlpatterns = [
    path('create-superuser/', SuperUserRegistrationView.as_view(), name='create-superuser'),
    path('register/customer/', CustomerRegistrationView.as_view(), name='customer_register'),
    path('register/vendor/', VendorRegistrationView.as_view(), name='vendor_register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('vendor/complete-profile/', VendorProfileCompletionView.as_view()),
    path('dashboard/customer/', CustomerDashboardView.as_view(), name='customer-dashboard'),
    path('dashboard/vendor/', VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('dashboard/captain/', CaptainDashboardView.as_view(), name='captain-dashboard'),
    path('activate/<str:uidb64>/<str:token>/',AccountActivationView.as_view(),name='activate' )
]