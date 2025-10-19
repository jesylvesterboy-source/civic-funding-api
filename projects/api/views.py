from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from django.http import HttpResponse
import pandas as pd
from ..models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=['get'])
    @permission_classes([permissions.AllowAny])
    def export_csv(self, request):
        # Export projects to CSV
        return Project.export_to_csv()

    @action(detail=False, methods=['get'])
    @permission_classes([permissions.AllowAny])
    def export_excel(self, request):
        # Export projects to Excel
        return Project.export_to_excel()

    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        # Import projects from CSV
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            imported_count = Project.import_from_csv(csv_file)
            return Response({
                'message': f'Successfully imported {imported_count} projects',
                'imported_count': imported_count
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    @permission_classes([permissions.AllowAny])
    def metrics(self, request):
        # Get project metrics for dashboard
        from django.db.models import Count, Sum, Avg
        from django.db.models import Q

        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status='active').count()
        completed_projects = Project.objects.filter(status='completed').count()
        total_budget = Project.objects.aggregate(total=Sum('budget'))['total'] or 0

        return Response({
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_budget': float(total_budget),
            'average_progress': Project.objects.aggregate(avg=Avg('progress'))['avg'] or 0
        })
