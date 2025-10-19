from rest_framework import viewsets
from ..models import MonitoringVisit, Report
from .serializers import MonitoringVisitSerializer, ReportSerializer

class MonitoringVisitViewSet(viewsets.ModelViewSet):
    queryset = MonitoringVisit.objects.all()
    serializer_class = MonitoringVisitSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
