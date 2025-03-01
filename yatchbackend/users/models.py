from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    ROLES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('captain', 'Captain'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='customer')
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'  # Use email as username
    REQUIRED_FIELDS = []  # Remove email from REQUIRED_FIELDS
    
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    company_name = models.CharField(max_length=100, unique=True)
    tax_id = models.CharField(max_length=30, unique=True)
    address = models.TextField()
    verified = models.BooleanField(default=False)
    
