from rest_framework import serializers
from .models import Distribution
class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = ['id','request_id','volunteer_id','scheduled_date','location','status','created_at']
        read_only_fields = ['id','status','created_at']
