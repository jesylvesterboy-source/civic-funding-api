from rest_framework import viewsets
from ..models import PerformanceIndicator
from .serializers import PerformanceIndicatorSerializer

class PerformanceIndicatorViewSet(viewsets.ModelViewSet):
    queryset = PerformanceIndicator.objects.all()
    serializer_class = PerformanceIndicatorSerializer
