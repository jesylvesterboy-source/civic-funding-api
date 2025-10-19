import pandas as pd
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Avg, Q, F, Max
from django.utils import timezone

class AnalyticsEngine:
    '''Engine for automated metrics computation and analytics'''
    
    @staticmethod
    def get_project_metrics():
        '''Get comprehensive project metrics'''
        from projects.models import Project
        from finances.models import Expense
        
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status='active').count()
        completed_projects = Project.objects.filter(status='completed').count()
        
        # Budget metrics
        budget_metrics = Project.objects.aggregate(
            total_budget=Sum('budget'),
            avg_budget=Avg('budget'),
            max_budget=Max('budget')
        )
        
        # Progress metrics
        progress_metrics = Project.objects.aggregate(
            avg_progress=Avg('progress'),
            on_track=Count('id', filter=Q(progress__gte=75)),
            behind=Count('id', filter=Q(progress__lt=50))
        )
        
        # Financial metrics
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        budget_utilization = (total_expenses / budget_metrics['total_budget'] * 100) if budget_metrics['total_budget'] else 0
        
        return {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_budget': float(budget_metrics['total_budget'] or 0),
            'average_budget': float(budget_metrics['avg_budget'] or 0),
            'average_progress': float(progress_metrics['avg_progress'] or 0),
            'projects_on_track': progress_metrics['on_track'],
            'projects_behind': progress_metrics['behind'],
            'total_expenses': float(total_expenses),
            'budget_utilization_rate': float(budget_utilization),
            'remaining_budget': float((budget_metrics['total_budget'] or 0) - total_expenses)
        }
    
    @staticmethod
    def get_farmer_metrics():
        '''Get comprehensive farmer metrics'''
        from farmers.models import Farmer, Household, FarmPlot
        
        total_farmers = Farmer.objects.count()
        total_households = Household.objects.count()
        total_farm_plots = FarmPlot.objects.count()
        
        # Gender distribution
        gender_stats = Farmer.objects.values('gender').annotate(count=Count('id'))
        gender_distribution = {stat['gender']: stat['count'] for stat in gender_stats}
        
        # Age analysis
        farmers_with_age = Farmer.objects.exclude(date_of_birth__isnull=True)
        age_stats = farmers_with_age.aggregate(
            young_farmers=Count('id', filter=Q(date_of_birth__gte=timezone.now() - timedelta(days=365*35))),
            experienced_farmers=Count('id', filter=Q(date_of_birth__lt=timezone.now() - timedelta(days=365*35)))
        )
        
        # Farm size analysis
        farm_size_stats = FarmPlot.objects.aggregate(
            total_land=Sum('size_acres'),
            avg_farm_size=Avg('size_acres'),
            largest_farm=Max('size_acres')
        )
        
        return {
            'total_farmers': total_farmers,
            'total_households': total_households,
            'total_farm_plots': total_farm_plots,
            'gender_distribution': gender_distribution,
            'average_farm_size': float(farm_size_stats['avg_farm_size'] or 0),
            'total_land_area': float(farm_size_stats['total_land'] or 0),
            'young_farmers': age_stats['young_farmers'],
            'experienced_farmers': age_stats['experienced_farmers']
        }
    
    @staticmethod
    def get_financial_metrics():
        '''Get comprehensive financial metrics'''
        from finances.models import Expense
        from projects.models import Project
        
        # Budget vs Actuals
        total_budget = Project.objects.aggregate(total=Sum('budget'))['total'] or 0
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        
        # Expense analysis by category
        expense_by_category = Expense.objects.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        # Monthly trends (last 6 months)
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_expenses = Expense.objects.filter(
            date__gte=six_months_ago
        ).extra({
            'month': 'strftime("%%Y-%%m", date)'
        }).values('month').annotate(
            monthly_total=Sum('amount')
        ).order_by('month')
        
        return {
            'total_budget': float(total_budget),
            'total_expenses': float(total_expenses),
            'budget_variance': float(total_budget - total_expenses),
            'utilization_rate': (total_expenses / total_budget * 100) if total_budget else 0,
            'expense_by_category': list(expense_by_category),
            'monthly_trends': list(monthly_expenses)
        }
    
    @staticmethod
    def get_performance_indicators():
        '''Get performance indicator metrics'''
        from indicators.models import PerformanceIndicator
        
        indicators = PerformanceIndicator.objects.all()
        indicator_data = {}
        
        for indicator in indicators:
            current_value = indicator.current_value or 0
            target_value = indicator.target_value or 1
            achievement_rate = (current_value / target_value * 100) if target_value else 0
            
            indicator_data[indicator.name] = {
                'current_value': float(current_value),
                'target_value': float(target_value),
                'achievement_rate': float(achievement_rate),
                'unit': indicator.unit,
                'status': 'Achieved' if achievement_rate >= 100 else 'In Progress'
            }
        
        return indicator_data
    
    @staticmethod
    def get_dashboard_summary():
        '''Get complete dashboard summary'''
        return {
            'projects': AnalyticsEngine.get_project_metrics(),
            'farmers': AnalyticsEngine.get_farmer_metrics(),
            'finances': AnalyticsEngine.get_financial_metrics(),
            'performance_indicators': AnalyticsEngine.get_performance_indicators(),
            'last_updated': timezone.now().isoformat()
        }
