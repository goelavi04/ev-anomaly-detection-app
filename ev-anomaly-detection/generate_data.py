import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Configuration
NUM_ROWS = 10000      # Changed from 100000
ANOMALY_RATE = 0.16   # Changed to 16%
# Generate base data
data = {
    'session_id': [fake.uuid4() for _ in range(NUM_ROWS)],
    'user_id': [random.randint(1000, 1050) for _ in range(NUM_ROWS)],
    'start_time': [fake.date_time_between(start_date='-1y', end_date='now') for _ in range(NUM_ROWS)],
    'energy_kWh': np.random.uniform(5.0, 75.0, NUM_ROWS).round(2),
    'ip_address': [fake.ipv4() for _ in range(NUM_ROWS)],
    'geo_location': [f"{fake.latitude()},{fake.longitude()}" for _ in range(NUM_ROWS)],
    'cpu_usage_percent': np.random.uniform(10, 40, NUM_ROWS).round(2),
    'packets_per_sec': np.random.randint(50, 200, NUM_ROWS)
}
df = pd.DataFrame(data)
df['end_time'] = df['start_time'] + df['energy_kWh'].apply(lambda x: timedelta(minutes=x * 1.5))
df['amount_INR'] = (df['energy_kWh'] * 18.5).round(2) # Assume a rate of ₹18.5/kWh
df['anomaly_type'] = 'none'

# --- Inject Anomalies ---
num_anomalies = int(NUM_ROWS * ANOMALY_RATE)
anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)

anomaly_types = ['payment_fraud', 'multi_user_conflict', 'dos_attack']
for i in anomaly_indices:
    anomaly = random.choice(anomaly_types)
    df.loc[i, 'anomaly_type'] = anomaly
    
    if anomaly == 'payment_fraud':
        # Unauthorized free charging
        df.loc[i, 'amount_INR'] = 0.0
    elif anomaly == 'dos_attack':
        # Simulate DoS attack with high CPU and packet rates
        df.loc[i, 'cpu_usage_percent'] = np.random.uniform(90, 100)
        df.loc[i, 'packets_per_sec'] = np.random.randint(1000, 5000)
    elif anomaly == 'multi_user_conflict':
        # Make another session for the same user overlap in time
        conflict_user_id = df.loc[i, 'user_id']
        conflict_start_time = df.loc[i, 'start_time'] + timedelta(minutes=5)
        # Find a different, non-anomaly row to inject the conflict
        potential_conflict_indices = df[(df.index != i) & (df['anomaly_type'] == 'none')].index
        if len(potential_conflict_indices) > 0:
            conflict_row_idx = np.random.choice(potential_conflict_indices)
            df.loc[conflict_row_idx, 'user_id'] = conflict_user_id
            df.loc[conflict_row_idx, 'start_time'] = conflict_start_time
            df.loc[conflict_row_idx, 'geo_location'] = f"{fake.latitude()},{fake.longitude()}" # Different location
            df.loc[conflict_row_idx, 'anomaly_type'] = 'multi_user_conflict'


# Save to CSV
df.to_csv('data/ev_charging_data.csv', index=False)
print(f"Generated data/ev_charging_data.csv with {NUM_ROWS} rows.")
print("Anomaly distribution:\n", df['anomaly_type'].value_counts())
