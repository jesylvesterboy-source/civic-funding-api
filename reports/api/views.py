from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from ..models import MonitoringVisit, Report
from .serializers import MonitoringVisitSerializer, ReportSerializer

class MonitoringVisitViewSet(viewsets.ModelViewSet):
    queryset = MonitoringVisit.objects.all()
    serializer_class = MonitoringVisitSerializer

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return MonitoringVisit.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return MonitoringVisit.export_to_excel()

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return Report.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return Report.export_to_excel()
