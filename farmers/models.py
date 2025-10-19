from django.db import models
from core.models import TimeStampedModel
from core.export_import import CustomExportMixin
from projects.models import Project

class Location(TimeStampedModel, CustomExportMixin):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria')

    def __str__(self):
        return f'{self.name}, {self.district}'

    @classmethod
    def export_to_csv(cls):
        'Export locations to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"locations.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'District', 'Region', 'Country'])
        
        for location in cls.objects.all():
            writer.writerow([
                location.name,
                location.district,
                location.region,
                location.country
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export locations to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for location in cls.objects.all():
            data.append({
                'Name': location.name,
                'District': location.district,
                'Region': location.region,
                'Country': location.country
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Locations', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"locations.xlsx\"'
        return response

class Household(TimeStampedModel, CustomExportMixin):
    head_of_household = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    family_size = models.PositiveIntegerField(default=1)
    income_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='low')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='households')

    def __str__(self):
        return self.head_of_household

    @classmethod
    def export_to_csv(cls):
        'Export households to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"households.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['Head of Household', 'Phone Number', 'Family Size', 'Income Level', 'Location', 'District', 'Region'])
        
        for household in cls.objects.all():
            writer.writerow([
                household.head_of_household,
                household.phone_number or '',
                household.family_size,
                household.income_level,
                household.location.name,
                household.location.district,
                household.location.region
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export households to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for household in cls.objects.all():
            data.append({
                'Head of Household': household.head_of_household,
                'Phone Number': household.phone_number or '',
                'Family Size': household.family_size,
                'Income Level': household.income_level,
                'Location': household.location.name,
                'District': household.location.district,
                'Region': household.location.region
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Households', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"households.xlsx\"'
        return response

class Farmer(TimeStampedModel, CustomExportMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    education_level = models.CharField(max_length=50, blank=True, null=True)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='farmers')
    projects = models.ManyToManyField(Project, related_name='farmers', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        # Calculate farmer age
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @classmethod
    def export_to_csv(cls):
        'Export farmers to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"farmers.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Gender', 'Age', 'Phone Number', 'Education Level', 'Household', 'Location', 'Projects Count'])
        
        for farmer in cls.objects.all():
            writer.writerow([
                farmer.first_name,
                farmer.last_name,
                farmer.gender,
                farmer.age or '',
                farmer.phone_number or '',
                farmer.education_level or '',
                farmer.household.head_of_household,
                farmer.household.location.name,
                farmer.projects.count()
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export farmers to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for farmer in cls.objects.all():
            data.append({
                'First Name': farmer.first_name,
                'Last Name': farmer.last_name,
                'Gender': farmer.gender,
                'Age': farmer.age or '',
                'Phone Number': farmer.phone_number or '',
                'Education Level': farmer.education_level or '',
                'Household': farmer.household.head_of_household,
                'Location': farmer.household.location.name,
                'Projects Count': farmer.projects.count()
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Farmers', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"farmers.xlsx\"'
        return response

class FarmPlot(TimeStampedModel, CustomExportMixin):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farm_plots')
    size_acres = models.DecimalField(max_digits=8, decimal_places=2)
    soil_type = models.CharField(max_length=50, blank=True, null=True)
    gps_coordinates = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='farm_plots', null=True, blank=True)

    def __str__(self):
        return f'{self.farmer} plot ({self.size_acres} acres)'

    @classmethod
    def export_to_csv(cls):
        'Export farm plots to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"farm_plots.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['Farmer', 'Size (Acres)', 'Soil Type', 'GPS Coordinates', 'Location'])
        
        for plot in cls.objects.all():
            writer.writerow([
                f'{plot.farmer.first_name} {plot.farmer.last_name}',
                plot.size_acres,
                plot.soil_type or '',
                plot.gps_coordinates or '',
                plot.location.name if plot.location else ''
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export farm plots to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for plot in cls.objects.all():
            data.append({
                'Farmer': f'{plot.farmer.first_name} {plot.farmer.last_name}',
                'Size (Acres)': plot.size_acres,
                'Soil Type': plot.soil_type or '',
                'GPS Coordinates': plot.gps_coordinates or '',
                'Location': plot.location.name if plot.location else ''
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Farm Plots', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"farm_plots.xlsx\"'
        return response
