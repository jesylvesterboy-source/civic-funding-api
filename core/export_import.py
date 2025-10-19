import csv
import pandas as pd
from django.http import HttpResponse
from io import StringIO, BytesIO

class ExportableModel:
    """Base class for models that can be exported - provides the interface"""
    
    @classmethod
    def export_to_csv(cls, queryset=None):
        """Base CSV export method - should be overridden by models"""
        raise NotImplementedError("Models must implement export_to_csv method")
    
    @classmethod
    def export_to_excel(cls, queryset=None):
        """Base Excel export method - should be overridden by models"""
        raise NotImplementedError("Models must implement export_to_excel method")

class AutoExportMixin(ExportableModel):
    """Mixin for automatic field-based export (uses all model fields)"""
    
    def to_csv_row(self):
        '''Convert model instance to CSV row using all fields'''
        return [str(getattr(self, field.name)) for field in self._meta.fields]

    @classmethod
    def get_csv_headers(cls):
        '''Get CSV headers from model fields'''
        return [field.verbose_name or field.name for field in cls._meta.fields]

    @classmethod
    def export_to_csv(cls, queryset=None):
        '''Export model data to CSV using all fields'''
        if queryset is None:
            queryset = cls.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{cls._meta.model_name}s.csv"'

        writer = csv.writer(response)
        writer.writerow(cls.get_csv_headers())

        for obj in queryset:
            writer.writerow(obj.to_csv_row())

        return response

    @classmethod
    def export_to_excel(cls, queryset=None):
        '''Export model data to Excel using all fields'''
        if queryset is None:
            queryset = cls.objects.all()

        data = []
        data.append(cls.get_csv_headers())

        for obj in queryset:
            data.append(obj.to_csv_row())

        df = pd.DataFrame(data[1:], columns=data[0])

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=cls._meta.verbose_name_plural[:31], index=False)

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{cls._meta.model_name}s.xlsx"'
        return response

class CustomExportMixin(ExportableModel):
    """Mixin for models that implement their own custom export methods"""
    
    # This mixin doesn't implement export methods - models must provide their own
    # It serves as a marker and provides the ExportableModel interface
    pass

# For backward compatibility
ExportImportMixin = AutoExportMixin
