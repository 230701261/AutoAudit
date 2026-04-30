from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from audit import views as audit_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Authentication ---
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='index.html'
    ), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    path('accounts/register/', audit_views.register_view, name='register'),

    # --- App URLs ---
    path('', include('audit.urls')),

    # --- Root URL → Redirect to login ---
    path('', auth_views.LoginView.as_view(
        template_name='index.html'
    )),
]