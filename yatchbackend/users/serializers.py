from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, VendorProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'phone', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role='customer'  # Auto-assign role
        )
        return user

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['company_name', 'tax_id', 'address']

class VendorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    vendor_profile = VendorProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'phone', 
                 'vendor_profile', 'first_name', 'last_name']

    def validate(self, attrs):
        # Check password match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        
        # Validate vendor profile data
        profile_data = attrs.get('vendor_profile', {})
        vendor_profile_serializer = VendorProfileSerializer(data=profile_data)
        if not vendor_profile_serializer.is_valid():
            raise serializers.ValidationError(vendor_profile_serializer.errors)
            
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        try:
            # Extract vendor profile data
            profile_data = validated_data.pop('vendor_profile')
            
            # Create user
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                phone=validated_data['phone'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                role='vendor'
            )
            
            # Create vendor profile
            VendorProfile.objects.create(user=user, **profile_data)
            
            return user
            
        except Exception as e:
            # Rollback transaction on any error
            raise serializers.ValidationError(
                {"detail": f"Registration failed: {str(e)}"}
            )
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['First_Name'] = user.first_name
        token['Last_Name'] = user.last_name
        token['role'] = user.role
        token['email'] = user.email
        token['phone'] = user.phone
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = {
            'id': self.user.id,
            'First_Name': self.user.first_name,
            'Last_name': self.user.last_name,
            'email': self.user.email,
            'role': self.user.role,
            'phone': self.user.phone
        }
        
        return data