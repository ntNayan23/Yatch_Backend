from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import VendorProfile

@receiver(post_save, sender=VendorProfile)
def handle_vendor_notifications(sender, instance, **kwargs):
    # Send admin notification when profile is submitted for approval
    if instance.submission_status == 'submitted' and instance.approval_status == 'pending':
        instance.send_admin_notification()
    
    # Send status update to vendor when approval status changes
    if 'approval_status' in kwargs.get('update_fields', []):
        instance.send_status_notification()