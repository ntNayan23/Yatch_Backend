from rest_framework import generics, status,permissions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.encoding import force_str
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from users.serializers import (
    CustomerRegistrationSerializer,
    VendorRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    VendorProfileSerializer,
    SuperUserRegistrationSerializer,
    VendorProfileCompletionSerializer,
)
from users.models import User
from users.permissions import IsAdminUserWithRole, IsVendor


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
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
        
        return Response({
            'user': {
                'id': user.id,
                'First_Name': user.first_name,
                'Last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'phone': user.phone
            },
            # 'vendor_profile': VendorProfileSerializer(user.vendor_profile).data
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    
class SuperUserRegistrationView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SuperUserRegistrationSerializer
    permission_classes = [IsAdminUserWithRole]  # Only existing admins can create superusers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': {
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
        }, status=status.HTTP_201_CREATED)
        
        
        
class VendorProfileCompletionView(generics.CreateAPIView):
    serializer_class = VendorProfileCompletionSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendor]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'vendor_profile'):
            raise ValidationError("Profile already exists")
        serializer.save(
            user=self.request.user,
            approval_status='pending'  # Wait for admin approval
        )
        
        
        
# class AccountActivationView(APIView):

class AccountActivationView(APIView):
    permission_classes = []  # Allow unauthenticated access

    def get(self, request, uidb64, token):
        try:
            # Decode UID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            # Validate token
            if default_token_generator.check_token(user, token):
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return Response(
                        {'detail': 'Account activated successfully'}, 
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {'detail': 'Account is already active'},
                    status=status.HTTP_200_OK
                )
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
            
        return Response(
            {'detail': 'Invalid activation link'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save(update_fields=['is_active'])
                user.save()
                return Response({'status': 'Account activated successfully'}, 
                              status=status.HTTP_200_OK)
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
            
        return Response({'error': 'Invalid activation link'}, 
                      status=status.HTTP_400_BAD_REQUEST)