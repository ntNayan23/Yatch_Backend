from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomerRegistrationView,
    VendorRegistrationView,
    LoginView
)
urlpatterns = [
    path('register/customer/', CustomerRegistrationView.as_view(), name='customer_register'),
    path('register/vendor/', VendorRegistrationView.as_view(), name='vendor_register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]