from rest_framework import serializers
from .models import AidRequest

class AidRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AidRequest
        fields = ['id','user_id','request_type','description','status','created_at']
        read_only_fields = ['id','status','created_at']
