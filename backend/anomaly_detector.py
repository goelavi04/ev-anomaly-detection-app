import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import os
import logging # Use logging instead of print for consistency

# Configure logging
logging.basicConfig(level=logging.DEBUG) # Set to DEBUG to see more info
logger = logging.getLogger(__name__)

# --- Path Calculation ---
# This assumes anomaly_detector.py is in the 'backend' folder
# and the main project structure is 'ev-anamoly-detection/ev-anomaly-detection/'
try:
    script_dir = Path(__file__).resolve().parent
    logger.debug(f"anomaly_detector.py script directory: {script_dir}")
    # Go up one level (to ev-anomaly-detection), then into 'ev-anomaly-detection' subfolder
    project_root = script_dir.parent
    logger.debug(f"Calculated project root directory: {project_root}")
    # Construct the model directory path relative to the project structure
    model_dir = project_root / 'ev-anomaly-detection' / 'models'
    logger.debug(f"Expecting models directory at: {model_dir}")

    # --- Debugging: Check if paths exist and list contents ---
    logger.debug(f"Does script_dir exist? {script_dir.exists()}")
    logger.debug(f"Does project_root exist? {project_root.exists()}")
    logger.debug(f"Does model_dir exist? {model_dir.exists()}")
    if model_dir.exists():
        logger.debug(f"Contents of model_dir ({model_dir}): {[p for p in model_dir.iterdir()]}")
    else:
        logger.error(f"model_dir ({model_dir}) does not exist.")
        raise FileNotFoundError(f"Models directory was NOT found at the calculated path: {model_dir}")

except Exception as e:
    logger.error(f"Error calculating paths: {e}")
    raise

# --- Load Models and Scalers ---
try:
    # Check individual file existence before loading
    dos_model_path = model_dir / "dos_model.pkl"
    dos_scaler_path = model_dir / "dos_scaler.pkl"
    fraud_model_path = model_dir / "fraud_model.pkl"
    fraud_scaler_path = model_dir / "fraud_scaler.pkl"

    required_files = [dos_model_path, dos_scaler_path, fraud_model_path, fraud_scaler_path]
    missing_files = [f for f in required_files if not f.exists()]

    if missing_files:
        logger.error(f"Missing required model/scaler files: {[str(f) for f in missing_files]}")
        raise FileNotFoundError(f"Missing required model/scaler files in {model_dir}")

    dos_model = joblib.load(dos_model_path)
    dos_scaler = joblib.load(dos_scaler_path)
    logger.debug("DoS model and scaler loaded.")

    fraud_model = joblib.load(fraud_model_path)
    fraud_scaler = joblib.load(fraud_scaler_path)
    logger.debug("Fraud model and scaler loaded.")

except FileNotFoundError as e: # Catch specific error first
     logger.error(f"Could not find required model/scaler files. Details: {e}")
     raise RuntimeError(f"Models not found in '{model_dir}'. Please ensure the Jupyter notebook was run successfully and models exist there.") from e
except Exception as e:
    logger.error(f"An unexpected error occurred loading models: {e}")
    raise RuntimeError(f"Failed to load models from '{model_dir}'.") from e

# --- Anomaly Detection Functions ---

def detect_multi_user_conflict(df):
    """Identifies sessions where a user's new session starts before their previous one ends."""
    logger.debug("Starting multi-user conflict detection.")
    required_cols = ['user_id', 'start_time', 'end_time', 'session_id']
    if not all(col in df.columns for col in required_cols):
        logger.warning(f"Skipping multi-user conflict: Missing one of {required_cols}")
        return []

    try:
        # Ensure correct data types (make copies to avoid SettingWithCopyWarning)
        df_sorted = df.copy()
        df_sorted['start_time'] = pd.to_datetime(df_sorted['start_time'], errors='coerce')
        df_sorted['end_time'] = pd.to_datetime(df_sorted['end_time'], errors='coerce')
        df_sorted = df_sorted.dropna(subset=['start_time', 'end_time']) # Drop rows where conversion failed

        df_sorted = df_sorted.sort_values(by=['user_id', 'start_time'])

        conflicts = df_sorted[
            (df_sorted['user_id'] == df_sorted['user_id'].shift(1)) &
            (df_sorted['start_time'] < df_sorted['end_time'].shift(1))
        ]
        conflict_ids = conflicts['session_id'].tolist()
        logger.debug(f"Found {len(conflict_ids)} multi-user conflicts.")
        return conflict_ids
    except Exception as e:
        logger.error(f"Error during multi-user conflict detection: {e}")
        return []


def find_anomalies(df: pd.DataFrame) -> dict:
    """
    Main function to run all anomaly detection checks on a DataFrame.
    Returns a dictionary: {"anomalies": list, "info": list}.
    """
    logger.info("Starting find_anomalies function.")
    # --- ADDED DEBUGGING ---
    logger.debug(f"Received DataFrame columns: {df.columns.tolist()}")
    logger.debug(f"Data types:\n{df.dtypes}")
    # -----------------------

    all_anomalies = []
    info_messages = []
    processed_session_ids = set() # Track processed IDs to avoid duplicates

    # --- Essential Column Check ---
    # These are absolutely needed for any processing
    essential_cols = ['session_id', 'start_time', 'end_time', 'user_id']
    missing_essential = [col for col in essential_cols if col not in df.columns]
    if missing_essential:
        msg = f"Essential columns missing after standardization: {missing_essential}. Cannot proceed."
        logger.error(msg)
        raise ValueError(msg) # Raise error to be caught by main.py

    try:
        # Convert time columns safely early on
        df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')
        df['end_time'] = pd.to_datetime(df['end_time'], errors='coerce')
    except Exception as e:
        msg = f"Error converting time columns: {e}. Cannot proceed."
        logger.error(msg)
        raise ValueError(msg)

    # 1. 💻 DoS Attack Detection
    dos_features = ['cpu_usage_percent', 'packets_per_sec']
    if all(col in df.columns for col in dos_features):
        logger.info("Attempting DoS detection...")
        try:
            # Select and ensure numeric type, coercing errors
            X_dos = df[dos_features].apply(pd.to_numeric, errors='coerce')
            valid_dos_rows = X_dos.dropna()

            if not valid_dos_rows.empty:
                X_dos_scaled = dos_scaler.transform(valid_dos_rows)
                dos_predictions = dos_model.predict(X_dos_scaled)

                # Map predictions back to original DataFrame index
                dos_anomaly_indices = valid_dos_rows.index[dos_predictions == -1]
                dos_anomalies_df = df.loc[dos_anomaly_indices]

                logger.info(f"DoS model predicted {len(dos_anomalies_df)} anomalies.")

                for index, row in dos_anomalies_df.iterrows():
                    session_id = row['session_id']
                    if session_id not in processed_session_ids:
                         all_anomalies.append({
                            'session_id': session_id,
                            'anomaly_type': 'dos_attack',
                            'timestamp': row['start_time'], # Keep as datetime for now
                            'details': f"CPU: {row.get('cpu_usage_percent', 'N/A')}%, Packets: {row.get('packets_per_sec', 'N/A')}/sec"
                        })
                         processed_session_ids.add(session_id)
            else:
                 logger.warning("No valid numeric data found for DoS detection after coercion.")

        except Exception as e:
            logger.error(f"Error during DoS detection: {e}")
            info_messages.append(f"DoS detection failed: {e}")
    else:
        msg = f"Skipping DoS detection: Missing one or more required columns ({dos_features})"
        logger.warning(msg)
        info_messages.append(msg)

    # 2. 💳 Billing Fraud Detection
    fraud_features = ['energy_kWh', 'amount_INR']
    if all(col in df.columns for col in fraud_features):
        logger.info("Attempting Billing Fraud detection...")
        try:
             # Select and ensure numeric type, coercing errors
            X_fraud = df[fraud_features].apply(pd.to_numeric, errors='coerce')
            valid_fraud_rows = X_fraud.dropna()

            if not valid_fraud_rows.empty:
                X_fraud_scaled = fraud_scaler.transform(valid_fraud_rows)
                fraud_predictions = fraud_model.predict(X_fraud_scaled)

                # Map predictions back to original DataFrame index
                fraud_anomaly_indices = valid_fraud_rows.index[fraud_predictions == -1]
                fraud_anomalies_df = df.loc[fraud_anomaly_indices]

                logger.info(f"Fraud model predicted {len(fraud_anomalies_df)} anomalies.")

                for index, row in fraud_anomalies_df.iterrows():
                    session_id = row['session_id']
                    if session_id not in processed_session_ids:
                         all_anomalies.append({
                            'session_id': session_id,
                            'anomaly_type': 'billing_fraud',
                            'timestamp': row['start_time'], # Keep as datetime
                            'details': f"Energy: {row.get('energy_kWh', 'N/A')} kWh, Amount: {row.get('amount_INR', 'N/A')} INR"
                        })
                         processed_session_ids.add(session_id)
                    else:
                        # Optionally: Add fraud details if session already flagged by DoS
                        for existing_anomaly in all_anomalies:
                            if existing_anomaly['session_id'] == session_id:
                                existing_anomaly['details'] += f"; Fraud: Energy: {row.get('energy_kWh', 'N/A')} kWh, Amount: {row.get('amount_INR', 'N/A')} INR"
                                existing_anomaly['anomaly_type'] += '+billing_fraud' # Combine types
                                break
            else:
                 logger.warning("No valid numeric data found for Fraud detection after coercion.")

        except Exception as e:
            logger.error(f"Error during Billing Fraud detection: {e}")
            info_messages.append(f"Billing Fraud detection failed: {e}")
    else:
        msg = f"Skipping Billing Fraud detection: Missing one or more required columns ({fraud_features})"
        logger.warning(msg)
        info_messages.append(msg)

    # 3. 👥 Multi-User Conflict Detection
    logger.info("Attempting Multi-User Conflict detection...")
    try:
        conflict_session_ids = detect_multi_user_conflict(df)
        conflict_anomalies_df = df[df['session_id'].isin(conflict_session_ids)]

        logger.info(f"Logic found {len(conflict_anomalies_df)} multi-user conflicts.")

        for index, row in conflict_anomalies_df.iterrows():
            session_id = row['session_id']
            if session_id not in processed_session_ids:
                all_anomalies.append({
                    'session_id': session_id,
                    'anomaly_type': 'multi_user_conflict',
                    'timestamp': row['start_time'], # Keep as datetime
                    'details': f"User: {row.get('user_id', 'N/A')}, Start: {row.get('start_time', 'N/A')}, End: {row.get('end_time', 'N/A')}"
                })
                processed_session_ids.add(session_id)
            else:
                 # Optionally: Add conflict details if session already flagged
                 for existing_anomaly in all_anomalies:
                     if existing_anomaly['session_id'] == session_id:
                         existing_anomaly['details'] += f"; Conflict: User: {row.get('user_id', 'N/A')}"
                         existing_anomaly['anomaly_type'] += '+multi_user_conflict' # Combine types
                         break
    except Exception as e:
        logger.error(f"Error during Multi-User Conflict processing: {e}")
        info_messages.append(f"Multi-User Conflict detection failed: {e}")


    # --- Timestamp Formatting for JSON ---
    logger.debug(f"Total anomalies detected before final formatting: {len(all_anomalies)}")
    final_anomalies = []
    for anomaly in all_anomalies:
         # Check if 'timestamp' is a valid datetime object before formatting
        if isinstance(anomaly.get('timestamp'), pd.Timestamp):
            anomaly['timestamp'] = anomaly['timestamp'].isoformat()
        else:
             # Handle cases where timestamp might be missing or invalid
             anomaly['timestamp'] = "Invalid/Missing Timestamp"
             logger.warning(f"Invalid or missing timestamp for session {anomaly.get('session_id', 'Unknown')}")
        final_anomalies.append(anomaly)

    logger.info(f"find_anomalies finished. Returning {len(final_anomalies)} anomalies and {len(info_messages)} info messages.")
    return {"anomalies": final_anomalies, "info": info_messages}

    

