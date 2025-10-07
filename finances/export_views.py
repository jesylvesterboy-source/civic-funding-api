import io
import csv
from datetime import datetime
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from openpyxl import Workbook
from .models import Budget, Expense, FinancialReport

class ExportBaseView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ExportBudgetsCSV(ExportBaseView):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="budgets_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Project', 'Budget Type', 'Allocated Amount', 'Total Expenses', 'Remaining', 'Utilization %'])
        
        budgets = Budget.objects.select_related('project').prefetch_related('expenses')
        for budget in budgets:
            writer.writerow([
                budget.project.name,
                budget.get_budget_type_display(),
                budget.allocated_amount,
                budget.total_expenses,
                budget.remaining_amount,
                f"{budget.utilization_percentage:.1f}%"
            ])
        
        return response

class ExportExpensesExcel(ExportBaseView):
    def get(self, request):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="expenses_{datetime.now().strftime("%Y%m%d")}.xlsx"'
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Expenses"
        
        # Headers
        headers = ['Project', 'Budget Type', 'Description', 'Amount', 'Date', 'Status', 'Payment Method']
        ws.append(headers)
        
        # Data
        expenses = Expense.objects.select_related('budget__project')
        for expense in expenses:
            ws.append([
                expense.budget.project.name,
                expense.budget.get_budget_type_display(),
                expense.description,
                expense.amount,
                expense.expense_date,
                expense.get_status_display(),
                expense.get_payment_method_display()
            ])
        
        wb.save(response)
        return response

class ExportFinancialReportPDF(ExportBaseView):
    def get(self, request, report_id):
        report = FinancialReport.objects.get(id=report_id)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="financial_report_{report.period_end.strftime("%Y%m%d")}.pdf"'
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title = Paragraph(f"Financial Report - {report.project.name}", styles['Title'])
        story.append(title)
        
        # Report details
        details_data = [
            ['Period', f"{report.period_start} to {report.period_end}"],
            ['Report Type', report.get_report_period_display()],
            ['Total Budget', f"${report.total_budget:,.2f}"],
            ['Total Expenses', f"${report.total_expenses:,.2f}"],
            ['Balance', f"${report.balance:,.2f}"],
            ['Utilization', f"{report.utilization_percentage:.1f}%"],
        ]
        
        details_table = Table(details_data, colWidths=[200, 200])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        story.append(details_table)
        
        if report.notes:
            notes = Paragraph(f"<b>Notes:</b> {report.notes}", styles['Normal'])
            story.append(notes)
        
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response