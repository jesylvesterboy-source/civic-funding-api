import csv
import pandas as pd
from django.http import HttpResponse
from io import StringIO, BytesIO
from django.core.files.base import ContentFile

class ExportImportMixin:
    '''Mixin to add CSV/Excel export and import functionality to models'''
    
    def to_csv_row(self):
        '''Convert model instance to CSV row'''
        return [str(getattr(self, field.name)) for field in self._meta.fields]
    
    @classmethod
    def get_csv_headers(cls):
        '''Get CSV headers from model fields'''
        return [field.name for field in cls._meta.fields]
    
    @classmethod
    def export_to_csv(cls, queryset=None):
        '''Export model data to CSV'''
        if queryset is None:
            queryset = cls.objects.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=\"{cls._meta.model_name}s.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(cls.get_csv_headers())
        
        for obj in queryset:
            writer.writerow(obj.to_csv_row())
        
        return response
    
    @classmethod
    def export_to_excel(cls, queryset=None):
        '''Export model data to Excel'''
        if queryset is None:
            queryset = cls.objects.all()
        
        data = []
        data.append(cls.get_csv_headers())
        
        for obj in queryset:
            data.append(obj.to_csv_row())
        
        df = pd.DataFrame(data[1:], columns=data[0])
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=cls._meta.verbose_name_plural, index=False)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=\"{cls._meta.model_name}s.xlsx\"'
        
        return response
    
    @classmethod
    def import_from_csv(cls, csv_file):
        '''Import model data from CSV'''
        decoded_file = csv_file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.reader(io_string)
        
        headers = next(reader)
        imported_count = 0
        
        for row in reader:
            if len(row) == len(headers):
                obj_data = dict(zip(headers, row))
                # Convert empty strings to None
                for key, value in obj_data.items():
                    if value == '':
                        obj_data[key] = None
                
                try:
                    obj = cls(**obj_data)
                    obj.save()
                    imported_count += 1
                except Exception as e:
                    print(f'Error importing {cls._meta.model_name}: {e}')
        
        return imported_count
