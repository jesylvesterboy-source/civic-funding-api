from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from ..models import PerformanceIndicator
from .serializers import PerformanceIndicatorSerializer

class PerformanceIndicatorViewSet(viewsets.ModelViewSet):
    queryset = PerformanceIndicator.objects.all()
    serializer_class = PerformanceIndicatorSerializer

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return PerformanceIndicator.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return PerformanceIndicator.export_to_excel()
