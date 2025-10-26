import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
import pymongo
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import io
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import traceback
import sys
import os

# Add backend directory to Python path to ensure imports work
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now import the anomaly detector at module level
from anomaly_detector import find_anomalies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("✅ Successfully imported find_anomalies from anomaly_detector.")

# --- Database Setup ---
MONGO_URI = "mongodb://localhost:27017/"
client = None
db = None
collection = None


# --- Custom JSON Encoder for ObjectId ---
def custom_jsonable_encoder(obj, **kwargs):
    """Encodes MongoDB ObjectIds and datetimes to strings."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return jsonable_encoder(obj, custom_encoder={ObjectId: str, datetime: lambda dt: dt.isoformat()}, **kwargs)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    global client, db, collection
    logger.info("Connecting to MongoDB...")
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        db = client["ev_anomaly_db"]
        collection = db["anomalies"]
        logger.info("✅ Successfully connected to MongoDB.")
    except pymongo.errors.ConnectionFailure as e:
        logger.error(f"❌ Could not connect to MongoDB: {e}")
        client = None
    yield
    # Code to run on shutdown
    if client:
        logger.info("Closing MongoDB connection.")
        client.close()


# --- Initialize FastAPI App (MUST BE AT MODULE LEVEL) ---
app = FastAPI(title="EV Anomaly Detection API", lifespan=lifespan)


# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",  # Added for your current frontend port
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- In-memory Log (Fallback if DB fails) ---
in_memory_log_store = []


# ✨ FLEXIBLE COLUMN MAPPER - Handles any CSV format
def standardize_columns(df):
    """
    Converts common CSV column name variations to a standard snake_case format
    required by the anomaly detection logic.
    """
    column_mapping = {
        # Session ID variations
        'sessionid': 'session_id', 'session id': 'session_id', 'session_id': 'session_id',
        'session_guid': 'session_id',

        # User ID variations
        'userid': 'user_id', 'user id': 'user_id', 'user_id': 'user_id',
        'customerid': 'user_id', 'customer id': 'user_id', 'customer_id': 'user_id',

        # Charger ID variations
        'chargerid': 'charger_id', 'charger id': 'charger_id', 'charger_id': 'charger_id',
        'chargingstationid': 'charger_id', 'charging station id': 'charger_id', 'charging_station_id': 'charger_id',
        'stationid': 'charger_id', 'station id': 'charger_id', 'station_id': 'charger_id',

        # Start Time variations
        'starttime': 'start_time', 'start time': 'start_time', 'start_time': 'start_time',
        'starttimestamp': 'start_time', 'start timestamp': 'start_time', 'start_timestamp': 'start_time',
        'timestamp': 'start_time',

        # End Time variations
        'endtime': 'end_time', 'end time': 'end_time', 'end_time': 'end_time',
        'endtimestamp': 'end_time', 'end timestamp': 'end_time', 'end_timestamp': 'end_time',

        # Duration variations
        'duration': 'duration', 'duration(min)': 'duration', 'duration_min': 'duration',
        'chargingtime': 'duration', 'charging time': 'duration', 'charging_time': 'duration',

        # Energy variations
        'energy': 'energy_kWh', 'energy(kwh)': 'energy_kWh', 'energy_kwh': 'energy_kWh',
        'energyconsumed': 'energy_kWh', 'energy consumed': 'energy_kWh', 'energy_consumed': 'energy_kWh',
        'kwh': 'energy_kWh', 'total kwh': 'energy_kWh', 'total_kwh': 'energy_kWh',

        # Payment/Amount variations
        'payment': 'amount_INR', 'amount': 'amount_INR', 'amountinr': 'amount_INR',
        'amount_inr': 'amount_INR', 'cost': 'amount_INR', 'totalcost': 'amount_INR',
        'total cost': 'amount_INR', 'total_cost': 'amount_INR',

        # IP Address variations
        'ipaddress': 'ip_address', 'ip address': 'ip_address', 'ip_address': 'ip_address',
        'sourceip': 'ip_address', 'source ip': 'ip_address', 'source_ip': 'ip_address',

        # CPU Usage variations
        'cpuusagepercent': 'cpu_usage_percent', 'cpu usage percent': 'cpu_usage_percent', 'cpu_usage_percent': 'cpu_usage_percent',
        'cpuusage': 'cpu_usage_percent', 'cpu usage': 'cpu_usage_percent', 'cpu_usage': 'cpu_usage_percent',
        'cpu %': 'cpu_usage_percent', 'cpu%': 'cpu_usage_percent',

        # Packets Per Second variations
        'packetspersec': 'packets_per_sec', 'packets per sec': 'packets_per_sec', 'packets_per_sec': 'packets_per_sec',
        'pps': 'packets_per_sec', 'packetrate': 'packets_per_sec', 'packet rate': 'packets_per_sec',
        'packet_rate': 'packets_per_sec',

        # Geolocation variations
        'geolocation': 'geo_location', 'geo location': 'geo_location', 'geo_location': 'geo_location',
        'location': 'geo_location', 'latlon': 'geo_location', 'lat/lon': 'geo_location',
        'coordinates': 'geo_location'
    }

    # Standardize column names
    original_columns = df.columns
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_', regex=False).str.replace('.', '_', regex=False)

    # Apply the mapping
    df = df.rename(columns=column_mapping, errors='ignore')

    # Log mapped columns
    mapped_cols = {orig: df.columns[i] for i, orig in enumerate(original_columns) 
                   if orig.lower().strip().replace(' ', '_').replace('.', '_') in column_mapping 
                   and i < len(df.columns) 
                   and df.columns[i] == column_mapping[orig.lower().strip().replace(' ', '_').replace('.', '_')]}
    if mapped_cols:
        logger.info(f"Standardized columns: {mapped_cols}")

    return df


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Accepts a CSV file, standardizes columns, runs detection, stores results,
    and returns findings ensuring JSON serializability.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        df_standardized = standardize_columns(df.copy())

        # Call find_anomalies (already imported at module level)
        detection_result = find_anomalies(df_standardized)

        # Ensure dict type and extract results safely
        if not isinstance(detection_result, dict):
            logger.error(f"Unexpected return type from find_anomalies: {type(detection_result)}. Expected dict.")
            detected_anomalies = []
            info_messages = ["Internal error: Anomaly detector returned unexpected format."]
        else:
            detected_anomalies = detection_result.get("anomalies", [])
            info_messages = detection_result.get("info", [])

        # Store anomalies
        if detected_anomalies:
            detection_timestamp = datetime.now()
            anomalies_to_insert = []
            for anomaly in detected_anomalies:
                if isinstance(anomaly, dict):
                    anomaly_copy = anomaly.copy()
                    anomaly_copy['detection_timestamp'] = detection_timestamp
                    anomalies_to_insert.append(anomaly_copy)
                else:
                    logger.warning(f"Skipping non-dict item in detected_anomalies: {anomaly}")

            if collection is not None and anomalies_to_insert:
                try:
                    collection.insert_many(anomalies_to_insert)
                    logger.info(f"Inserted {len(anomalies_to_insert)} anomalies into MongoDB.")
                except Exception as db_e:
                    logger.error(f"Failed to insert anomalies into MongoDB: {db_e}")
            elif collection is None:
                logger.warning("DB not connected, skipping log storage.")

        # Prepare response
        response_data = {
            "filename": file.filename,
            "total_sessions": len(df),
            "anomalies_found": len(detected_anomalies),
            "anomalies": detected_anomalies,
            "info": info_messages
        }
        return custom_jsonable_encoder(response_data)

    except ValueError as ve:
        logger.error(f"Value Error during prediction processing: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"An unexpected error occurred during prediction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.get("/logs/")
async def get_logs():
    """Fetches all detected anomalies from the database, ensuring JSON serializability."""
    if collection is not None:
        try:
            logs_from_db = list(collection.find({}, {'_id': 0}).sort("detection_timestamp", pymongo.DESCENDING))
            logger.info(f"Fetched {len(logs_from_db)} logs from MongoDB.")
            serializable_logs = custom_jsonable_encoder(logs_from_db)
            return {"anomalies": serializable_logs}
        except Exception as db_e:
            logger.error(f"Failed to fetch logs from MongoDB: {db_e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to fetch logs from database.")
    else:
        logger.warning("DB not connected, cannot fetch historical logs.")
        return {"anomalies": [], "info": "Database not connected."}


@app.get("/")
async def root():
    return {"message": "EV Anomaly Detection API is running"}