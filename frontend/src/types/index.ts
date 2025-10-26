export interface Anomaly {
  session_id: string;
  anomaly_type: 'dos_attack' | 'billing_fraud' | 'multi_user_conflict';
  timestamp: string;
  user_id?: string;
  charging_station_id?: string;
  energy_consumed?: number;
  amount_billed?: number;
  duration?: number;
  details?: Record<string, any>;
}

export interface PredictResponse {
  filename: string;
  total_sessions: number;
  anomalies_found: number;
  anomalies: Anomaly[];
}

export interface LogsResponse {
  anomalies: Anomaly[];
}

export interface AnomalyStats {
  total: number;
  dos_attack: number;
  billing_fraud: number;
  multi_user_conflict: number;
}