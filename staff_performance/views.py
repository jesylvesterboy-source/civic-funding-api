# staff_performance/views.py
import csv
import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Avg, Count, Sum
from django.contrib import messages
from django.urls import reverse

from .models import StaffMember, PerformanceMetric, PerformanceReview, KeyPerformanceIndicator
from .forms import PerformanceMetricUploadForm

class StaffPerformanceDashboard(LoginRequiredMixin, TemplateView):
    """Staff Performance Dashboard"""
    template_name = 'staff_performance/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Performance statistics
        total_staff = StaffMember.objects.filter(is_active=True).count()
        avg_performance = StaffMember.objects.filter(is_active=True).aggregate(
            avg_score=Avg('overall_performance_score')
        )['avg_score'] or 0
        
        # Top performers
        top_performers = StaffMember.objects.filter(
            is_active=True
        ).order_by('-overall_performance_score')[:5]
        
        # Department performance
        department_stats = StaffMember.objects.filter(
            is_active=True
        ).values('department').annotate(
            avg_score=Avg('overall_performance_score'),
            staff_count=Count('id')
        )
        
        context.update({
            'total_staff': total_staff,
            'avg_performance': avg_performance,
            'top_performers': top_performers,
            'department_stats': department_stats,
        })
        return context

class StaffList(LoginRequiredMixin, ListView):
    """List all staff members"""
    model = StaffMember
    template_name = 'staff_performance/staff_list.html'
    context_object_name = 'staff_members'
    
    def get_queryset(self):
        return StaffMember.objects.filter(is_active=True).select_related('user')

class StaffDetail(LoginRequiredMixin, DetailView):
    """Staff member detail view"""
    model = StaffMember
    template_name = 'staff_performance/staff_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'staff_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.object
        
        # Performance metrics
        metrics = staff.performance_metrics.all().order_by('-period_end')
        
        # Recent reviews
        reviews = staff.performance_reviews.all().order_by('-review_date')[:5]
        
        context.update({
            'metrics': metrics,
            'reviews': reviews,
        })
        return context

class PerformanceMetricList(LoginRequiredMixin, ListView):
    """List performance metrics"""
    model = PerformanceMetric
    template_name = 'staff_performance/metric_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return PerformanceMetric.objects.select_related('staff__user').all()

class PerformanceReviewList(LoginRequiredMixin, ListView):
    """List performance reviews"""
    model = PerformanceReview
    template_name = 'staff_performance/review_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return PerformanceReview.objects.select_related('staff__user', 'reviewer__user').all()

class KPIList(LoginRequiredMixin, ListView):
    """List key performance indicators"""
    model = KeyPerformanceIndicator
    template_name = 'staff_performance/kpi_list.html'
    
    def get_queryset(self):
        return KeyPerformanceIndicator.objects.filter(is_active=True)

class PerformanceReport(LoginRequiredMixin, TemplateView):
    """Performance report view"""
    template_name = 'staff_performance/performance_report.html'

# Function-based views
def export_performance_metrics(request):
    """Export performance metrics to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="performance_metrics.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Staff Name', 'Metric Name', 'Category', 'Target', 'Actual', 'Achievement Rate', 'Period End'])
    
    metrics = PerformanceMetric.objects.select_related('staff__user').all()
    for metric in metrics:
        writer.writerow([
            metric.staff.user.get_full_name(),
            metric.metric_name,
            metric.get_metric_category_display(),
            metric.target_value,
            metric.actual_value,
            metric.achievement_rate,
            metric.period_end.strftime('%Y-%m-%d')
        ])
    
    return response

def upload_performance_metrics(request):
    """Upload performance metrics via CSV"""
    if request.method == 'POST':
        form = PerformanceMetricUploadForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, 'Metrics uploaded successfully!')
            return redirect('staff_performance:metric_list')
    else:
        form = PerformanceMetricUploadForm()
    
    return render(request, 'staff_performance/upload_metrics.html', {'form': form})

def export_kpis(request):
    """Export KPIs to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="organizational_kpis.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['KPI Name', 'Department', 'Type', 'Target', 'Current', 'Achievement %', 'Status'])
    
    kpis = KeyPerformanceIndicator.objects.filter(is_active=True)
    for kpi in kpis:
        writer.writerow([
            kpi.name,
            kpi.get_department_display(),
            kpi.get_kpi_type_display(),
            kpi.target_value,
            kpi.current_value,
            kpi.achievement_percentage,
            kpi.status
        ])
    
    return response

def export_performance_report(request):
    """Export comprehensive performance report"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="performance_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Staff Name', 'Department', 'Position', 'Performance Score', 'Last Review'])
    
    staff_members = StaffMember.objects.filter(is_active=True).select_related('user')
    for staff in staff_members:
        writer.writerow([
            staff.user.get_full_name(),
            staff.get_department_display(),
            staff.position_title,
            staff.overall_performance_score,
            staff.last_performance_review.strftime('%Y-%m-%d') if staff.last_performance_review else 'Never'
        ])
    
    return response
