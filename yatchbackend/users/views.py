from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomerRegistrationSerializer, VendorRegistrationSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'First_Name': user.first_name,
                'Last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            }
        }, status=status.HTTP_201_CREATED)

class VendorRegistrationView(generics.CreateAPIView):
    serializer_class = VendorRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'First_Name': user.first_name,
                'Last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            },
            'vendor_profile': VendorProfileSerializer(user.vendor_profile).data
            # 'tokens': {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token)
            # }
        }, status=status.HTTP_201_CREATED)
        

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer