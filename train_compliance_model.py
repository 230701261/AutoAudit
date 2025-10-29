# train_compliance_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib # For saving models
from pathlib import Path

# --- Configuration ---
DATA_FILE = "bank_statement.xlsx"
MODEL_DIR = Path("audit") / "ml_models" # Save models inside your 'audit' app
MODEL_DIR.mkdir(parents=True, exist_ok=True) # Create directory if it doesn't exist
GST_MODEL_FILE = MODEL_DIR / "gst_compliance_model.pkl"
TDS_MODEL_FILE = MODEL_DIR / "tds_compliance_model.pkl"

# -----------------------------
# 1. Load Data
# -----------------------------
print("🔹 Loading data...")
try:
    data = pd.read_excel(DATA_FILE)
    print("✅ Data Loaded Successfully!")
    print("Shape:", data.shape)
    # print(data.head(), "\n") # Optional: uncomment to see data head
except FileNotFoundError:
    print(f"❌ Error: Data file '{DATA_FILE}' not found. Place it in the same directory as this script.")
    exit() # Stop if data isn't found
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

# -----------------------------
# 2. Encode Categorical Features
# -----------------------------
print("🔹 Encoding features...")
# --- IMPORTANT: Save the mapping for consistent encoding later ---
# We'll use pandas factorize which returns codes and the unique categories (index)
data['Business_Sector_Code'], business_sector_map = pd.factorize(data['Business_Sector'])
# Save the mapping (optional but good practice)
# joblib.dump(business_sector_map, MODEL_DIR / "business_sector_map.pkl")
print("✅ Features Encoded.")

# -----------------------------
# 3. Prepare Features and Targets
# -----------------------------
# --- Use the new encoded column ---
feature_cols = ["Total_Transactions", "Detected_Anomalies", "Compliance_Score", "Business_Sector_Code"]
target_gst_col = "GST_Compliance"
target_tds_col = "TDS_Compliance"

# Check if columns exist
missing_cols = [col for col in feature_cols + [target_gst_col, target_tds_col] if col not in data.columns]
if missing_cols:
    print(f"❌ Error: The following required columns are missing from '{DATA_FILE}': {', '.join(missing_cols)}")
    exit()

X = data[feature_cols]
y_gst = data[target_gst_col]
y_tds = data[target_tds_col]

# -----------------------------
# 4. Split Dataset
# -----------------------------
print("🔹 Splitting data...")
try:
    # Stratify if targets might be imbalanced
    stratify_targets = pd.concat([y_gst, y_tds], axis=1) if not y_gst.empty and not y_tds.empty else None
    X_train, X_test, y_gst_train, y_gst_test, y_tds_train, y_tds_test = train_test_split(
        X, y_gst, y_tds, test_size=0.2, random_state=42, stratify=stratify_targets
    )
    print("✅ Data Split.")
except ValueError as e:
    print(f"❌ Error splitting data (check target distributions or test_size): {e}")
    exit()


# -----------------------------
# 5. Train Models
# -----------------------------
print("🔹 Training GST model...")
# Added class_weight for potential imbalance, n_estimators for slight performance boost
gst_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
gst_model.fit(X_train, y_gst_train)
print("✅ GST Model Trained.")

print("🔹 Training TDS model...")
# Added class_weight for potential imbalance, n_estimators for slight performance boost
tds_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
tds_model.fit(X_train, y_tds_train)
print("✅ TDS Model Trained.")

# -----------------------------
# 6. Evaluation (Optional, but good for checking training)
# -----------------------------
print("\n📊 Evaluating models on test set...")
gst_pred = gst_model.predict(X_test)
tds_pred = tds_model.predict(X_test)

gst_acc = accuracy_score(y_gst_test, gst_pred)
tds_acc = accuracy_score(y_tds_test, tds_pred)
print(f"Test Set GST Compliance Accuracy: {gst_acc:.3f}")
print(f"Test Set TDS Compliance Accuracy: {tds_acc:.3f}\n")

print("GST Classification Report (Test Set):")
print(classification_report(y_gst_test, gst_pred, zero_division=0))
print("TDS Classification Report (Test Set):")
print(classification_report(y_tds_test, tds_pred, zero_division=0))

# -----------------------------
# 7. Save Models
# -----------------------------
print(f"🔹 Saving GST model to {GST_MODEL_FILE}...")
joblib.dump(gst_model, GST_MODEL_FILE)
print("✅ GST Model Saved.")

print(f"🔹 Saving TDS model to {TDS_MODEL_FILE}...")
joblib.dump(tds_model, TDS_MODEL_FILE)
print("✅ TDS Model Saved.")

print("\n🎉 Training and saving complete!")