# staff_performance/forms.py
from django import forms
from .models import PerformanceMetric

class PerformanceMetricUploadForm(forms.Form):
    """Form for uploading performance metrics via CSV"""
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with performance metrics data'
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('Please upload a CSV file')
        return csv_file

class StaffPerformanceFilterForm(forms.Form):
    """Form for filtering staff performance data"""
    department = forms.ChoiceField(
        choices=[('', 'All Departments')] + PerformanceMetric.METRIC_CATEGORIES,
        required=False,
        label='Department'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='From Date'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='To Date'
    )
