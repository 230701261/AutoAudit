# audit/ml_compliance.py
import joblib
import pandas as pd
from pathlib import Path
from django.conf import settings # To get BASE_DIR

# --- Model Loading ---
BASE_DIR = settings.BASE_DIR
MODEL_DIR = BASE_DIR / "audit" / "ml_models"
GST_MODEL_FILE = MODEL_DIR / "gst_compliance_model.pkl"
TDS_MODEL_FILE = MODEL_DIR / "tds_compliance_model.pkl"

GST_MODEL = None
TDS_MODEL = None

# It's better to load models once when the server starts if possible,
# but loading on first request is also common.
def load_models():
    """ Load the saved ML models into memory. """
    global GST_MODEL, TDS_MODEL
    if GST_MODEL is None:
        try:
            GST_MODEL = joblib.load(GST_MODEL_FILE)
            print("✅ GST Compliance model loaded.")
        except FileNotFoundError:
            print(f"❌ Error: GST Model file not found at {GST_MODEL_FILE}")
        except Exception as e:
            print(f"❌ Error loading GST model: {e}")

    if TDS_MODEL is None:
        try:
            TDS_MODEL = joblib.load(TDS_MODEL_FILE)
            print("✅ TDS Compliance model loaded.")
        except FileNotFoundError:
            print(f"❌ Error: TDS Model file not found at {TDS_MODEL_FILE}")
        except Exception as e:
            print(f"❌ Error loading TDS model: {e}")

# Call load_models() once when this module is imported (when Django server starts)
load_models()


# --- Prediction Function ---
def predict_compliance(data_df):
    """
    Makes GST and TDS compliance predictions on a DataFrame.

    Args:
        data_df (pd.DataFrame): DataFrame containing new data with columns:
                                 'Total_Transactions', 'Detected_Anomalies',
                                 'Compliance_Score', 'Business_Sector'.

    Returns:
        pd.DataFrame: Original DataFrame with added prediction columns
                      'GST_Prediction', 'TDS_Prediction', or None if error.
    """
    if GST_MODEL is None or TDS_MODEL is None:
        print("❌ Error: Models are not loaded. Cannot predict.")
        # Optionally, try loading again
        load_models()
        if GST_MODEL is None or TDS_MODEL is None:
             print("❌ Error: Failed to load models on demand.")
             return None # Indicate failure

    # Define required columns for features + the categorical column for encoding
    required_feature_cols = ["Total_Transactions", "Detected_Anomalies", "Compliance_Score"]
    categorical_col = "Business_Sector"
    all_required_cols = required_feature_cols + [categorical_col]

    missing_cols = [col for col in all_required_cols if col not in data_df.columns]
    if missing_cols:
        print(f"❌ Error: Input data missing required columns: {', '.join(missing_cols)}")
        return None

    try:
        # 1. Preprocess - MUST match training preprocessing *exactly*
        print("🔹 Preprocessing data for prediction...")
        # Use factorize again. Assumes categories in new data might overlap with training data.
        # For robustness, load a saved mapping from training if available.
        data_df['Business_Sector_Code'], _ = pd.factorize(data_df[categorical_col])
        print("✅ Preprocessing complete.")

        # 2. Select Features (Ensure order matches training)
        feature_cols_for_prediction = required_feature_cols + ['Business_Sector_Code']
        X_predict = data_df[feature_cols_for_prediction]

        # 3. Predict
        print("🔹 Making predictions...")
        gst_predictions = GST_MODEL.predict(X_predict)
        tds_predictions = TDS_MODEL.predict(X_predict)
        print("✅ Predictions complete.")

        # 4. Add predictions to DataFrame
        data_df['GST_Prediction'] = gst_predictions
        data_df['TDS_Prediction'] = tds_predictions

        return data_df

    except KeyError as e:
         print(f"❌ Error: Missing column during prediction preprocessing or feature selection: {e}")
         return None
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None # Indicate failure