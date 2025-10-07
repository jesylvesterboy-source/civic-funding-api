from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'budgets', views.BudgetViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'financial-reports', views.FinancialReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]