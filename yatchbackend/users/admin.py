from django.contrib import admin
from .models import VendorProfile, User
from django.contrib import messages
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active')
    actions = ['resend_activation']

    def resend_activation(self, request, queryset):
        for user in queryset.filter(is_active=False):
            user.send_activation_email()
        self.message_user(request, f"Activation emails sent to {queryset.count()} users")
    
    resend_activation.short_description = "Resend activation email"

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'tax_id', 'approval_status', 'created_at','user_active_status', 'profile_completion')
    list_filter = ('submission_status','approval_status', 'created_at')
    search_fields = ('company_name', 'tax_id', 'user__email')
    actions = ['approve_vendors', 'reject_vendors']
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Vendor Email'
    
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(submission_status='submitted')
        return qs
    
    def user_active_status(self, obj):
        return obj.user.is_active
    user_active_status.boolean = True
    user_active_status.short_description = 'Account Active'


    def approve_vendors(self, request, queryset):
        # Only process vendors that are pending approval
        to_approve = queryset.filter(approval_status='pending')
        updated = to_approve.count()
        to_approve.update(approval_status='approved')
        
        messages.success(
            request,
            f'Approved {updated} vendor(s). '
            f'{queryset.count() - updated} were already approved.'
        )
            
    def reject_vendors(self, request, queryset):
        # Only process vendors that are approved/pending
        to_reject = queryset.exclude(approval_status='rejected')
        updated = to_reject.count()
        to_reject.update(approval_status='rejected')
        
        messages.warning(
            request,
            f'Rejected {updated} vendor(s). '
            f'{queryset.count() - updated} were already rejected.'
        )


    approve_vendors.short_description = "Approve selected vendors"
    reject_vendors.short_description = "Reject selected vendors"