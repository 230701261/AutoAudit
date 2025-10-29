# audit/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Use carefully for testing
from django.views.decorators.http import require_POST
import json
import pandas as pd
from .ml_compliance import predict_compliance # Import prediction function

# --- Plotting Imports ---
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend suitable for web servers
import matplotlib.pyplot as plt
import seaborn as sns # Added for distribution plot
import io # Input/Output operations for saving plot in memory
import base64 # For encoding plot image
import traceback # For detailed error logging

# --- Configure Google AI (Hardcoded Key - INSECURE) ---
try:
    # --- HARDCODE YOUR API KEY HERE ---
    GOOGLE_API_KEY = "AIzaSyBwVWVw8jrew0MAlumsr5_aQOBoEW70f-s" # <-- YOUR KEY HERE
    # --- --- --- --- --- --- --- --- ---

    if not GOOGLE_API_KEY:
        print("Warning: GOOGLE_API_KEY is not set in the code.")
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error configuring Google AI: {e}")
    GOOGLE_API_KEY = None # Ensure key is None if config fails


# --- Authentication Views ---

def index_view(request):
    """ Handles the login page (root URL). """
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
    """ Handles the registration page. """
    if request.user.is_authenticated:
        return redirect('dashboard')
    # Add actual registration logic here using UserCreationForm if needed
    return render(request, 'RegisterPage.html')


# --- Chatbot API View ---
@csrf_exempt
@require_POST
def chatbot_api_view(request):
    """ API endpoint for the chatbot """
    if not GOOGLE_API_KEY:
         return JsonResponse({'error': 'Chatbot not configured (API key missing or invalid).'}, status=500)

    ai_response_text = "Error: AI response not generated."
    response = None

    try:
        data = json.loads(request.body)
        user_message = data.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided.'}, status=400)

        model = genai.GenerativeModel('gemini-pro') # Using gemini-pro
        response = model.generate_content(user_message)

        try:
             ai_response_text = response.text
        except ValueError:
             print(f"Chatbot response blocked: {response.prompt_feedback}")
             block_reason = "Unknown"
             if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                 block_reason = response.prompt_feedback.block_reason.name
             ai_response_text = f"Response blocked due to: {block_reason}"
        except Exception as e:
             print(f"Error accessing response text parts: {e}")
             ai_response_text = "Error processing AI response content."

        return JsonResponse({'response': ai_response_text})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
    except Exception as e:
        print(f"Error in chatbot API view processing: {e}")
        error_message = f"An internal error occurred while contacting the AI: {str(e)}"
        if response and hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
            error_message = f"Request blocked due to: {response.prompt_feedback.block_reason.name}"
        return JsonResponse({'error': error_message}, status=500)


# --- ML Compliance Check API View ---
@csrf_exempt
@require_POST
@login_required
def finance_compliance_check_api(request):
    """ API endpoint to run the finance compliance ML check. """
    try:
        data = json.loads(request.body)
        print(f"Received data for compliance check: {data}")
        if not data:
             return JsonResponse({'error': 'No input data provided.'}, status=400)

        data_df_single = pd.DataFrame([data])
        result_df = predict_compliance(data_df_single)
        if result_df is None:
            print("Compliance check failed: predict_compliance returned None")
            return JsonResponse({'error': 'Compliance check failed.'}, status=500)

        result = result_df.to_dict(orient='records')[0]
        result.pop('Business_Sector_Code', None)
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        print(f"Unexpected error in compliance API view: {e}")
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)


# --- File Upload View for ML ---
@login_required
def data_upload_view(request):
    """ Handles GET to show form & POST to process Excel OR CSV file with plots. """
    context = {}
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            context['error_message'] = 'No file was uploaded.'
            return render(request, 'Data UploadPage.html', context)

        uploaded_file = request.FILES['excel_file']
        filename = uploaded_file.name
        is_csv = filename.lower().endswith('.csv')
        is_xlsx = filename.lower().endswith('.xlsx')

        if not is_csv and not is_xlsx:
            context['error_message'] = 'Invalid file type. Please upload an .xlsx or .csv file.'
            return render(request, 'Data UploadPage.html', context)

        data_df = None

        # --- Step 1: Try Reading the File ---
        try:
            print(f"🔹 Reading uploaded file: {filename}")
            if is_xlsx:
                data_df = pd.read_excel(uploaded_file, engine='openpyxl')
            else: # Must be CSV
                try:
                    uploaded_file.seek(0)
                    data_df = pd.read_csv(uploaded_file)
                except UnicodeDecodeError:
                     uploaded_file.seek(0)
                     data_df = pd.read_csv(uploaded_file, encoding='latin-1')
            print("✅ File read successfully.")

        except Exception as e:
            error_msg = f'Error reading file ({filename}): {e}'
            if is_xlsx and ("Invalid filter: 'replace'" in str(e) or "Unsupported filter" in str(e)):
                 error_msg = ("Error reading Excel file: Unsupported feature (like filters) found. "
                              "Please ensure filters are removed, or save as CSV and re-upload.")
            elif isinstance(e, pd.errors.ParserError):
                 error_msg = f"Error parsing CSV file: {e}. Ensure it's a valid CSV."
            elif isinstance(e, UnicodeDecodeError):
                 error_msg = f"Encoding error reading file: {e}. Try saving the CSV with UTF-8 encoding."
            print(f"❌ {error_msg}")
            context['error_message'] = error_msg
            return render(request, 'Data UploadPage.html', context)

        # --- Step 2: Try Processing and Predicting ---
        if data_df is not None:
            results_df = None
            try:
                # --- Run Prediction ---
                results_df = predict_compliance(data_df.copy())

                if results_df is None:
                    context['error_message'] = 'Error running ML prediction. Check input data columns/types.'
                    print("❌ Error: predict_compliance returned None.")
                    return render(request, 'Data UploadPage.html', context)

                # --- Generate Plots ---
                print("🔹 Generating plots...")
                context['plots'] = {} # Use a dictionary to store multiple plots
                plot_error_messages = []

                # --- Plot 1: Prediction Summary Bar Chart ---
                if 'GST_Prediction' in results_df and 'TDS_Prediction' in results_df:
                    try:
                        fig1, ax1 = plt.subplots(1, 2, figsize=(10, 4))
                        # GST
                        gst_counts = results_df['GST_Prediction'].value_counts().sort_index()
                        gst_labels = gst_counts.index.map({0:'Non-Compliant', 1:'Compliant'})
                        ax1[0].bar(gst_labels, gst_counts.values, color=['red', 'green'][:len(gst_labels)])
                        ax1[0].set_title('Predicted GST Compliance')
                        ax1[0].set_ylabel('Count')
                        for i, v in enumerate(gst_counts.values):
                            ax1[0].text(i, v + 0.5, str(v), ha='center', va='bottom')

                        # TDS
                        tds_counts = results_df['TDS_Prediction'].value_counts().sort_index()
                        tds_labels = tds_counts.index.map({0:'Non-Compliant', 1:'Compliant'})
                        ax1[1].bar(tds_labels, tds_counts.values, color=['red', 'green'][:len(tds_labels)])
                        ax1[1].set_title('Predicted TDS Compliance')
                        ax1[1].set_ylabel('Count')
                        for i, v in enumerate(tds_counts.values):
                             ax1[1].text(i, v + 0.5, str(v), ha='center', va='bottom')

                        plt.tight_layout()
                        buffer = io.BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        graphic_summary = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        buffer.close()
                        plt.close(fig1)
                        context['plots']['summary_bar'] = graphic_summary
                        print("✅ Summary Plot generated.")
                    except Exception as plot_err:
                        print(f"⚠️ Error generating Summary Plot: {plot_err}")
                        plot_error_messages.append("Could not generate summary plot.")
                else:
                     print("⚠️ Could not generate Summary Plot: Prediction columns missing.")

                # --- Plot 2: Scatter Plot (Score vs Anomalies) ---
                if 'Compliance_Score' in results_df and 'Detected_Anomalies' in results_df and 'GST_Prediction' in results_df:
                    try:
                        fig2 = plt.figure(figsize=(8, 6))
                        colors = results_df['GST_Prediction'].map({0: 'red', 1: 'green'})
                        plt.scatter(results_df['Detected_Anomalies'], results_df['Compliance_Score'], c=colors, alpha=0.6)
                        plt.title('Compliance Score vs. Detected Anomalies (Colored by GST Prediction)')
                        plt.xlabel('Detected Anomalies')
                        plt.ylabel('Compliance Score')
                        handles = [plt.Line2D([0], [0], marker='o', color='w', label='Non-Compliant', markersize=10, markerfacecolor='red'),
                                   plt.Line2D([0], [0], marker='o', color='w', label='Compliant', markersize=10, markerfacecolor='green')]
                        plt.legend(handles=handles, title="GST Prediction")
                        plt.grid(True, linestyle='--', alpha=0.5)
                        plt.tight_layout()
                        buffer = io.BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        graphic_scatter = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        buffer.close()
                        plt.close(fig2)
                        context['plots']['scatter_score_anomaly'] = graphic_scatter
                        print("✅ Scatter Plot generated.")
                    except Exception as plot_err:
                        print(f"⚠️ Error generating Scatter Plot: {plot_err}")
                        plot_error_messages.append("Could not generate scatter plot.")
                else:
                    print("⚠️ Could not generate Scatter Plot: Required columns missing.")

                # --- Plot 3: Distribution Plot (Compliance Score) ---
                if 'Compliance_Score' in results_df:
                    try:
                        fig3 = plt.figure(figsize=(8, 4))
                        sns.histplot(results_df['Compliance_Score'], kde=True, bins=15)
                        plt.title('Distribution of Compliance Scores')
                        plt.xlabel('Compliance Score')
                        plt.ylabel('Frequency')
                        plt.tight_layout()
                        buffer = io.BytesIO()
                        plt.savefig(buffer, format='png')
                        buffer.seek(0)
                        graphic_dist = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        buffer.close()
                        plt.close(fig3)
                        context['plots']['distribution_score'] = graphic_dist
                        print("✅ Distribution Plot generated.")
                    except Exception as plot_err:
                        print(f"⚠️ Error generating Distribution Plot: {plot_err}")
                        plot_error_messages.append("Could not generate score distribution plot.")
                else:
                    print("⚠️ Could not generate Distribution Plot: Compliance_Score column missing.")

                if plot_error_messages:
                    context['plot_error_message'] = "; ".join(plot_error_messages)

                # --- Prepare results list safely ---
                print("🔹 Preparing results for display...")
                display_columns = [col for col in results_df.columns if col != 'Business_Sector_Code']
                results_list = results_df[display_columns].to_dict(orient='records')
                print("✅ Results prepared.")

                context['results'] = results_list
                context['filename'] = filename

                # --- Success: Render results page ---
                return render(request, 'compliance_results.html', context)

            except Exception as e:
                # Handle errors during prediction, plotting, or results prep
                error_msg = f'Error processing data after reading: {e}'
                print(f"❌ {error_msg}")
                print("\n--- Full Traceback ---")
                traceback.print_exc()
                print("--- End Traceback ---\n")
                context['error_message'] = error_msg
                return render(request, 'Data UploadPage.html', context)
        else:
             context['error_message'] = 'Failed to load data frame from file.'
             return render(request, 'Data UploadPage.html', context)

    # For GET request
    return render(request, 'Data UploadPage.html', context)


# --- Protected Application Page Views ---
@login_required
def dashboard_view(request):
    """ Serves the main dashboard page. """
    return render(request, 'dashboard.html')

@login_required
def transactions_view(request):
    """ Serves the transactions monitoring page. """
    return render(request, 'transactions.html')

@login_required
def anomalies_view(request):
    """ Serves the anomaly center page. """
    return render(request, 'anomalies.html')

@login_required
def compliance_view(request):
    """ Serves the compliance command centre page. """
    return render(request, 'compliance.html')

@login_required
def reports_view(request):
    """ Serves the reports and insights page. """
    return render(request, 'reports.html')

@login_required
def rules_management_view(request):
    """ Serves the rules management page. """
    return render(request, 'Rules ManagementPage.html')

@login_required
def assign_reviewer_view(request):
    """ Serves the assign reviewer page. """
    return render(request, 'Assign Reviewer Page.html')

@login_required
def transaction_detail_view(request):
    """ Serves the transaction detail page. """
    return render(request, 'Transaction Detail Page.html')

@login_required
def audit_trail_view(request): # Added view for Audit Trail
    """ Serves the audit trail page. """
    return render(request, 'Audit TrailPage.html')