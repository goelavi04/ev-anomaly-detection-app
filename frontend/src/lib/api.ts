import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface BackendAnomaly {
  session_id: string;
  anomaly_type: 'dos_attack' | 'billing_fraud' | 'multi_user_conflict';
  timestamp: string;
  user_id?: string;
  charging_station_id?: string;
  energy_consumed?: number;
  amount_billed?: number;
  duration?: number;
}

export interface PredictResponse {
  filename: string;
  total_sessions: number;
  anomalies_found: number;
  anomalies: BackendAnomaly[];
}

export interface LogsResponse {
  anomalies: BackendAnomaly[];
}

export const api = {
  // Upload CSV and get predictions
  uploadAndPredict: async (file: File): Promise<PredictResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post<PredictResponse>(
      `${API_BASE_URL}/predict/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  // Fetch all logs from MongoDB
  fetchLogs: async (): Promise<LogsResponse> => {
    const response = await axios.get<LogsResponse>(`${API_BASE_URL}/logs/`);
    return response.data;
  },
};