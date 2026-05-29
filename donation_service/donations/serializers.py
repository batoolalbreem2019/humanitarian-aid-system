from rest_framework import serializers
from .models import Donation
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id','donor_user_id','request_id','amount','status','donated_at']
        read_only_fields = ['id','status','donated_at']
