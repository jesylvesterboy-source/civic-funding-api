from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from core.analytics import AnalyticsEngine

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_metrics(request):
    'Get comprehensive dashboard metrics'
    try:
        metrics = AnalyticsEngine.get_dashboard_summary()
        return Response(metrics)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
