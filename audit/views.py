# audit/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm  # ✅ NEW (IMPORTANT)

import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json
import pandas as pd
from .ml_compliance import predict_compliance
from pathlib import Path

# --- Plotting Imports ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import traceback


# --- Configure Google AI ---
try:
    GOOGLE_API_KEY = "AIzaSyBwVWVw8jrew0MAlumsr5_aQOBoEW70f-s"  # ⚠️ Replace or move to .env
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)
    else:
        print("Warning: GOOGLE_API_KEY not set.")
except Exception as e:
    print(f"Error configuring Google AI: {e}")
    GOOGLE_API_KEY = None


# =========================================================
# 🔐 AUTHENTICATION
# =========================================================

def index_view(request):
    """Login page"""
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
                next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard'
                return redirect(next_url)
    else:
        form = AuthenticationForm()

    next_url = request.GET.get('next', '')
    return render(request, 'index.html', {'form': form, 'next': next_url})


def register_view(request):
    """Registration with real Django user creation"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'RegisterPage.html', {'form': form})


# =========================================================
# 🤖 CHATBOT API
# =========================================================

@csrf_exempt
@require_POST
def chatbot_api_view(request):
    if not GOOGLE_API_KEY:
        return JsonResponse({'error': 'Chatbot not configured.'}, status=500)

    try:
        data = json.loads(request.body)
        user_message = data.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)

        try:
            return JsonResponse({'response': response.text})
        except:
            return JsonResponse({'response': 'Blocked or empty response'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# =========================================================
# 📊 ML COMPLIANCE API
# =========================================================

@csrf_exempt
@require_POST
@login_required
def finance_compliance_check_api(request):
    try:
        data = json.loads(request.body)

        if not data:
            return JsonResponse({'error': 'No input data'}, status=400)

        df = pd.DataFrame([data])
        result_df = predict_compliance(df)

        if result_df is None:
            return JsonResponse({'error': 'Prediction failed'}, status=500)

        result = result_df.to_dict(orient='records')[0]
        result.pop('Business_Sector_Code', None)

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# =========================================================
# 📁 FILE UPLOAD + ML + PLOTS
# =========================================================

@login_required
def data_upload_view(request):
    context = {}

    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            context['error_message'] = 'No file uploaded'
            return render(request, 'Data UploadPage.html', context)

        file = request.FILES['excel_file']
        filename = file.name

        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

        except Exception as e:
            context['error_message'] = str(e)
            return render(request, 'Data UploadPage.html', context)

        try:
            results_df = predict_compliance(df)

            context['results'] = results_df.to_dict(orient='records')
            context['filename'] = filename

            return render(request, 'compliance_results.html', context)

        except Exception as e:
            context['error_message'] = str(e)
            return render(request, 'Data UploadPage.html', context)

    return render(request, 'Data UploadPage.html', context)


# =========================================================
# 📄 POLICY UPLOAD
# =========================================================

@login_required
def upload_policy_view(request):
    context = {}

    if request.method == 'POST':
        policy_name = request.POST.get('policy_name')
        policy_file = request.FILES.get('policy_file')

        if policy_name and policy_file:
            context['message'] = "Policy uploaded successfully"
            context['success'] = True
        else:
            context['message'] = "Missing data"
            context['success'] = False

    return render(request, 'upload_policy.html', context)


# =========================================================
# 📋 CHECKLIST
# =========================================================

@login_required
def checklist_view(request):
    return render(request, 'checklist_view.html')


# =========================================================
# 📊 PROTECTED PAGES
# =========================================================

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def transactions_view(request):
    return render(request, 'transactions.html')

@login_required
def anomalies_view(request):
    return render(request, 'anomalies.html')

@login_required
def compliance_view(request):
    return render(request, 'compliance.html')

@login_required
def reports_view(request):
    return render(request, 'reports.html')

@login_required
def rules_management_view(request):
    return render(request, 'Rules ManagementPage.html')

@login_required
def assign_reviewer_view(request):
    return render(request, 'Assign Reviewer Page.html')

@login_required
def transaction_detail_view(request):
    return render(request, 'Transaction Detail Page.html')

@login_required
def audit_trail_view(request):
    return render(request, 'Audit TrailPage.html')

@login_required
def gst_checklist_view(request):
    return render(request, 'gst_checklist.html')

@login_required
def tds_checklist_view(request):
    return render(request, 'tds_checklist.html')

@login_required
def company_law_checklist_view(request):
    return render(request, 'company_law_checklist.html')