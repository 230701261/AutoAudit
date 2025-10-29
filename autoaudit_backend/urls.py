# autoaudit_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from audit import views as audit_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Authentication ---
    path('accounts/register/', audit_views.register_view, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # --- Redirect old default login URL ---
    path('accounts/login/', RedirectView.as_view(pattern_name='index', permanent=False)),

    # --- App URLs ---
    # Includes dashboard, transactions, anomalies, compliance, reports,
    # data_upload, rules_management, assign_reviewer, transaction_detail,
    # api/chatbot, api/compliance-check
    path('', include('audit.urls')),

    # --- Root URL (Login Page) ---
    path('', audit_views.index_view, name='index'),

    # --- (Optional Safety Net for login name) ---
    path('', audit_views.index_view, name='login'),
]