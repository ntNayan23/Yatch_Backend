from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User, VendorProfile, CustomerProfile, CaptainProfile

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
            role='customer',
            is_active=False
        )
        user.send_activation_email()
        CustomerProfile.objects.create(user=user)
        return user

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['company_name', 'tax_id', 'address']

class VendorRegistrationSerializer(serializers.ModelSerializer):
    
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
        fields = ['email', 'password', 'password2', 'phone', 
                  'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        
        # profile_data = attrs.get('vendor_profile', {})
        # vendor_profile_serializer = VendorProfileSerializer(data=profile_data)
        # if not vendor_profile_serializer.is_valid():
        #     raise serializers.ValidationError(vendor_profile_serializer.errors)
            
        return attrs
    
    # def validate_tax_id(self, value):
    #     if not value.startswith('TAX-'):
    #         raise serializers.ValidationError("Tax ID must start with TAX-")
    #     return value

    @transaction.atomic
    def create(self, validated_data):
        try:
            
            # Create inactive user until admin approval
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                phone=validated_data['phone'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                role='vendor',
                is_active=False  # Disable login until approved
            )
            user.send_activation_email()
            # Create vendor profile with pending status
            # vendor_profile = VendorProfile.objects.create(
            #     user=user,
            #     approval_status='pending',  # Initial approval status
            #     **profile_data
            # )
            
            # Here you would typically send an email notification to admins
            # Example: send_approval_request_email(user, vendor_profile)
            
            return user
            
        except Exception as e:
            raise serializers.ValidationError(
                {"detail": f"Registration failed: {str(e)}"}
            )

class VendorProfileCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['company_name', 'tax_id', 'address']
        extra_kwargs = {
            'company_name': {'required': True},
            'tax_id': {'required': True}
        }

    def validate_tax_id(self, value):
        if not value.startswith('TAX-'):
            raise serializers.ValidationError("Tax ID must start with TAX-")
        return value

class CaptainRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    license_number = serializers.CharField(write_only=True, required=True)
    available_from = serializers.TimeField(required=True)
    available_to = serializers.TimeField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'phone', 
                'first_name', 'last_name', 'license_number',
                'available_from', 'available_to']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        try:
            license_number = validated_data.pop('license_number')
            available_from = validated_data.pop('available_from')
            available_to = validated_data.pop('available_to')

            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                phone=validated_data['phone'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                role='captain'
            )
            CaptainProfile.objects.create(
                user=user,
                license_number=license_number,
                available_from=available_from,
                available_to=available_to
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"detail": f"Registration failed: {str(e)}"})


class SuperUserRegistrationSerializer(serializers.ModelSerializer):
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
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'is_staff': {'default': True},
            'is_superuser': {'default': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_superuser(
            role='admin',  # Force admin role
            **validated_data
        )
    
    
    
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials'),
        'account_inactive': _('This account is not activated. Check your email.'),
        'invalid_role': _('User role not recognized')
    }

    @classmethod
    def get_token(cls, user):  # Corrected method signature
        # Validate user role before token creation
        if user.role not in dict(user.ROLES).keys():
            raise serializers.ValidationError(
                cls.default_error_messages['invalid_role'],
                code='invalid_role'
            )
            
        token = super().get_token(user)
        
        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.role
        token['email'] = user.email
        token['phone'] = user.phone
        
        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password']
        }
        
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Check authentication and activation status
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError(
                self.default_error_messages['no_active_account'],
                code='no_active_account'
            )

        if not self.user.is_active:
            raise serializers.ValidationError(
                self.default_error_messages['account_inactive'],
                code='account_inactive'
            )

        # Validate user role
        if self.user.role not in dict(self.user.ROLES).keys():
            raise serializers.ValidationError(
                self.default_error_messages['invalid_role'],
                code='invalid_role'
            )

        data = super().validate(attrs)
        
        # Add user details to response
        data['user'] = {
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'role': self.user.role,
            'phone': self.user.phone
        }
        
        return data