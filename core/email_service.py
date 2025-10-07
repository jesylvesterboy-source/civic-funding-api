from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_expense_approval_notification(expense, approver):
    """Send notification when expense needs approval"""
    subject = f"Expense Approval Required - {expense.budget.project.name}"
    
    context = {
        'expense': expense,
        'approver': approver,
        'project': expense.budget.project,
        'amount': expense.amount,
    }
    
    html_message = render_to_string('emails/expense_approval_request.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[approver.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_expense_approved_notification(expense):
    """Send notification when expense is approved"""
    subject = f"Expense Approved - {expense.budget.project.name}"
    
    context = {
        'expense': expense,
        'project': expense.budget.project,
        'amount': expense.amount,
        'approved_by': expense.approved_by,
    }
    
    html_message = render_to_string('emails/expense_approved.html', context)
    plain_message = strip_tags(html_message)
    
    # Notify the person who created the expense
    recipient = expense.budget.created_by.email
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        html_message=html_message,
        fail_silently=False,
    )

def send_budget_alert_notification(budget, threshold=80):
    """Send notification when budget utilization exceeds threshold"""
    utilization = budget.utilization_percentage
    
    if utilization >= threshold:
        subject = f"Budget Alert: {budget.budget_type} - {budget.project.name}"
        
        context = {
            'budget': budget,
            'utilization': utilization,
            'threshold': threshold,
            'project': budget.project,
        }
        
        html_message = render_to_string('emails/budget_alert.html', context)
        plain_message = strip_tags(html_message)
        
        # Notify project manager and finance officers
        recipients = [budget.created_by.email]
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            html_message=html_message,
            fail_silently=False,
        )