from rest_framework import serializers
from .models import AccidentEvent

class AccidentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccidentEvent
        fields = ['id', 'device_id', 'impact', 'distance', 'vibration', 'raw_message', 'created_at']
        read_only_fields = ['id', 'created_at']

    # If you want to allow missing distance/vibration but require impact:
    impact = serializers.FloatField()
    distance = serializers.FloatField(required=False, allow_null=True)
    vibration = serializers.IntegerField(required=False, allow_null=True)
    device_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    raw_message = serializers.CharField(required=False, allow_blank=True, allow_null=True)
