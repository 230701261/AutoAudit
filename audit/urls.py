# audit/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- API URLs ---
    # ... (chatbot_api, compliance_check_api) ...

    # --- Page URLs ---
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('anomalies/', views.anomalies_view, name='anomalies'),
    path('compliance/', views.compliance_view, name='compliance'),
    path('reports/', views.reports_view, name='reports'),
    path('data-upload/', views.data_upload_view, name='data_upload'),
    path('rules-management/', views.rules_management_view, name='rules_management'),
    path('assign-reviewer/', views.assign_reviewer_view, name='assign_reviewer'),
    path('transaction-detail/', views.transaction_detail_view, name='transaction_detail'),
    path('audit-trail/', views.audit_trail_view, name='audit_trail'),
    path('upload-policy/', views.upload_policy_view, name='upload_policy'),
    # path('checklist/', views.checklist_view, name='checklist_view'), # Remove or keep generic one if needed
    path('checklist/gst/', views.gst_checklist_view, name='gst_checklist'), # <-- Add
    path('checklist/tds/', views.tds_checklist_view, name='tds_checklist'), # <-- Add
    path('checklist/company-law/', views.company_law_checklist_view, name='company_law_checklist'), # <-- Add
]