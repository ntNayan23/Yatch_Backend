from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.validators import RegexValidator

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
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
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
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be in format: '+999999999'")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def local_created_at(self):
        return timezone.localtime(self.created_at) 
    @property
    def local_Updated_at(self):
        return timezone.localtime(self.updated_at) 
    
    USERNAME_FIELD = 'email'  # Use email as username
    REQUIRED_FIELDS = []  # Remove email from REQUIRED_FIELDS
    
    objects = CustomUserManager()
    
    def send_activation_email(self):
        token = default_token_generator.make_token(self)
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        
        subject = 'Activate Your Account'
        message = (
            f'Please click the link to activate your account:\n\n'
            f'{settings.FRONTEND_URL}/activate/{uid}/{token}/'
        )
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.email} ({self.role})"


class VendorProfile(models.Model):
    approval_status = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    company_name = models.CharField(max_length=100, unique=True, blank=True)
    tax_id = models.CharField(max_length=30, unique=True, blank=True)
    address = models.TextField(blank=True)
    approval_status  = models.CharField(
        max_length=10, 
        choices=approval_status, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    profile_completion = models.PositiveIntegerField(default=0)
    submission_status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('submitted', 'Submitted')],
        default='draft'
    )
    
    
    REQUIRED_FIELDS = ['company_name', 'tax_id', 'address']
    
    @property
    def local_created_at(self):
        return timezone.localtime(self.created_at) 
    
    # def save(self, *args, **kwargs):
    #     if self.pk:  # Only on update
    #         original = VendorProfile.objects.get(pk=self.pk)
    #         if original.approval_status != self.approval_status:
    #             self.send_status_notification()
    #     super().save(*args, **kwargs)
    def update_completion(self):
        completed = sum(1 for field in self.REQUIRED_FIELDS if getattr(self, field))
        self.profile_completion = int((completed / len(self.REQUIRED_FIELDS))) * 100
        self.save()
        
        
    def save(self, *args, **kwargs):
        # Get original state before saving
        if self.pk:
            original = VendorProfile.objects.get(pk=self.pk)
            if original.approval_status != self.approval_status:
                self.send_status_notification()
            
        super().save(*args, **kwargs)

        # Update user active status based on approval
        # self.user.is_active = self.approval_status == 'approved'
        # self.user.save(update_fields=['is_active'])
        
        # Send notification only if status changed

            
            
    def send_admin_notification(self):
        subject = f"New Vendor Submission: {self.company_name}"
        message = f"Vendor {self.company_name} has submitted their profile for approval."
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL],  # Use settings instead of hardcoded email
            fail_silently=False,
        )

    def send_status_notification(self):
        subject = f"Vendor Status Update - {self.company_name}"
        message = f"Your approval status: {self.get_approval_status_display()}"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )
        
        
    
    def __str__(self):
        return f"{self.company_name} - {self.get_approval_status_display()}"
    
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def local_created_at(self):
        return timezone.localtime(self.created_at) 
    
    @property
    def local_Updated_at(self):
        return timezone.localtime(self.updated_at) 


class CaptainProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='captain_profile')
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    certifications = models.JSONField(default=list)  # Stores list of certifications
    available_from = models.TimeField()
    available_to = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def local_created_at(self):
        return timezone.localtime(self.created_at) 
    
    @property
    def local_Updated_at(self):
        return timezone.localtime(self.updated_at) 
