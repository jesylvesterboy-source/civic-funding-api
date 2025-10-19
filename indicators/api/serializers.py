from rest_framework import serializers
from ..models import PerformanceIndicator

class PerformanceIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceIndicator
        fields = '__all__'
