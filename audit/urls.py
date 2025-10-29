# audit/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- API URLs ---
    path('api/chatbot/', views.chatbot_api_view, name='chatbot_api'),
    path('api/compliance-check/', views.finance_compliance_check_api, name='compliance_check_api'),

    # --- Page URLs ---
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('anomalies/', views.anomalies_view, name='anomalies'),
    path('compliance/', views.compliance_view, name='compliance'),
    path('reports/', views.reports_view, name='reports'),
    path('data-upload/', views.data_upload_view, name='data_upload'), # View handles both GET and POST
    path('rules-management/', views.rules_management_view, name='rules_management'),
    path('assign-reviewer/', views.assign_reviewer_view, name='assign_reviewer'),
    path('transaction-detail/', views.transaction_detail_view, name='transaction_detail'),
    path('audit-trail/', views.audit_trail_view, name='audit_trail'), # Added URL for audit trail
]