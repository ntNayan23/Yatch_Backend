from rest_framework import serializers
from django.db.models import Sum
from ..models import User, VendorProfile

class CustomerDashboardSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()
    upcoming_trips = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'phone', 'total_bookings', 'upcoming_trips']

    def get_total_bookings(self, obj):
        try:
            return obj.bookings.count()
        except AttributeError:
            return 0

    def get_upcoming_trips(self, obj):
        try:
            return obj.bookings.filter(status='upcoming').count()
        except AttributeError:
            return 0

class VendorDashboardSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    total_yachts = serializers.SerializerMethodField()
    total_earnings = serializers.SerializerMethodField()
    approval_status = serializers.CharField()
    
    class Meta:
        model = VendorProfile
        fields = '__all__'

    def get_total_yachts(self, obj):
        try:
            return obj.user.yachts.count()
        except AttributeError:
            return 0

    def get_total_earnings(self, obj):
        try:
            if hasattr(obj.user.bookings.model, 'total_price'):
                return obj.user.bookings.aggregate(total=Sum('total_price'))['total'] or 0
            return 0
        except AttributeError:
            return 0

class CaptainDashboardSerializer(serializers.ModelSerializer):
    upcoming_assignments = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'upcoming_assignments', 'availability']

    def get_upcoming_assignments(self, obj):
        try:
            return obj.assignments.filter(status='scheduled').count()
        except AttributeError:
            return 0

    def get_availability(self, obj):
        try:
            profile = obj.captain_profile
            return f"{profile.available_from} - {profile.available_to}"
        except AttributeError:
            return "Not available"