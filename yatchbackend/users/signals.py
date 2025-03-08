from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import VendorProfile

@receiver(post_save, sender=VendorProfile)
def notify_admin_on_vendor_registration(sender, instance, created, **kwargs):
    if created:
        # Send email notification to admin
        from django.core.mail import send_mail
        send_mail(
            'New Vendor Approval Request',
            f'New vendor registration from {instance.company_name} and needs approval.',
            'nayanthakre379@gmail.com',
            ['nayanthakre379@gmail.com'],
            fail_silently=False,
        )
    else:
        if 'approval_status' in kwargs.get('update_fields', []):
            instance.send_status_notification()