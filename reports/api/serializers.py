from rest_framework import serializers
from ..models import MonitoringVisit, Report

class MonitoringVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringVisit
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
