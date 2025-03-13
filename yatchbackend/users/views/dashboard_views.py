from rest_framework import generics
from users.serializers import (
    CustomerDashboardSerializer,
    VendorDashboardSerializer,
    CaptainDashboardSerializer
)
from users.permissions import IsCustomer, IsVendor, IsCaptain,IsApprovedVendor

class CustomerDashboardView(generics.RetrieveAPIView):
    serializer_class = CustomerDashboardSerializer
    permission_classes = [IsCustomer]

    def get_object(self):
        return self.request.user

class VendorDashboardView(generics.RetrieveAPIView):
    serializer_class = VendorDashboardSerializer
    permission_classes = [IsVendor]
    # permission_classes = [IsApprovedVendor]

    def get_object(self):
        return self.request.user.vendor_profile

class CaptainDashboardView(generics.RetrieveAPIView):
    serializer_class = CaptainDashboardSerializer
    permission_classes = [IsCaptain]

    def get_object(self):
        return self.request.user.captain_profile