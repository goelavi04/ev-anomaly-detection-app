import { BackendAnomaly } from './api';
import type { EVSession } from '../components/EVDashboard';

export function transformBackendAnomalyToSession(anomaly: BackendAnomaly): EVSession {
  // Map backend anomaly types to frontend format
  const anomalyTypeMap = {
    'dos_attack': 'dos' as const,
    'billing_fraud': 'fraud' as const,
    'multi_user_conflict': 'multiuser' as const,
  };

  const anomalyType = anomalyTypeMap[anomaly.anomaly_type];

  // Determine status based on anomaly type
  let status: 'critical' | 'warning' | 'normal' = 'normal';
  let score = 0;

  if (anomaly.anomaly_type === 'billing_fraud') {
    status = 'critical';
    score = 0.95;
  } else if (anomaly.anomaly_type === 'dos_attack') {
    status = 'critical';
    score = 0.92;
  } else if (anomaly.anomaly_type === 'multi_user_conflict') {
    status = 'warning';
    score = 0.75;
  }

  return {
    sessionId: anomaly.session_id,
    chargerId: anomaly.charging_station_id || `CH${Math.floor(Math.random() * 60) + 1}`,
    startTime: new Date(anomaly.timestamp).toLocaleTimeString(),
    duration: anomaly.duration || 0,
    energy: anomaly.energy_consumed || 0,
    score,
    anomalyType,
    status,
    userId: anomaly.user_id || 'Unknown',
    payment: anomaly.amount_billed,
  };
}