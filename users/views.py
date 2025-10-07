from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import project_manager_required, finance_officer_required
from projects.models import Project
from farmers.models import Farmer
from reports.models import Report

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }
    
    # Role-based dashboard data
    if user.can_manage_projects:
        context['projects_count'] = Project.objects.count()
        context['recent_projects'] = Project.objects.all()[:5]
    
    if user.can_manage_finances:
        context['farmers_count'] = Farmer.objects.count()
    
    if user.can_view_reports:
        context['recent_reports'] = Report.objects.all()[:5]
    
    return render(request, 'users/dashboard.html', context)