import { useState } from "react";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { ScrollArea } from "./ui/scroll-area";
import { Badge } from "./ui/badge";
import { Database, RefreshCw, Calendar, Search, Loader2 } from "lucide-react";
import { Input } from "./ui/input";
import { toast } from "sonner";
import { api } from "../lib/api";
import { transformBackendAnomalyToSession } from "../lib/transformers";
import type { EVSession } from "./EVDashboard";

interface LogsViewerProps {
  onLoadLog: (sessions: EVSession[]) => void;
}

interface LogEntry {
  _id: string;
  timestamp: string;
  sessionCount: number;
  anomalyCount: number;
  sessions: EVSession[];
}

export function LogsViewer({ onLoadLog }: LogsViewerProps) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const fetchLogsFromMongoDB = async () => {
    setIsLoading(true);
    
    try {
      // Fetch from real backend
      const response = await api.fetchLogs();
      
      // Transform backend data to frontend format
      const transformedSessions = response.anomalies.map(transformBackendAnomalyToSession);
      
      // Create a single log entry with all the data
      const logEntry: LogEntry = {
        _id: `log_${Date.now()}`,
        timestamp: new Date().toLocaleString(),
        sessionCount: transformedSessions.length,
        anomalyCount: transformedSessions.filter(s => s.anomalyType !== null).length,
        sessions: transformedSessions
      };
      
      setLogs([logEntry, ...logs]);
      
      toast.success(`Fetched ${transformedSessions.length} sessions from MongoDB`);
    } catch (error: any) {
      console.error('Failed to fetch logs:', error);
      
      if (error.response) {
        toast.error(
          `Failed to fetch logs: ${error.response.data.detail || 'Server error'}`,
          { description: 'Check if your backend server is running' }
        );
      } else if (error.request) {
        toast.error(
          'Cannot connect to backend server',
          { description: 'Make sure your FastAPI server is running on http://localhost:8000' }
        );
      } else {
        toast.error('Failed to fetch logs', { description: error.message });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const filteredLogs = logs.filter(log => 
    log._id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    log.timestamp.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Card className="bg-slate-900 border-slate-800 p-6">
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database className="w-6 h-6 text-blue-400" />
            <div>
              <h2 className="text-xl text-white font-semibold">Previous Logs</h2>
              <p className="text-sm text-slate-400">MongoDB Archive</p>
            </div>
          </div>
          <Button 
            onClick={fetchLogsFromMongoDB}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Loading...
              </>
            ) : (
              <>
                <RefreshCw className="w-4 h-4 mr-2" />
                Fetch Logs
              </>
            )}
          </Button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Search logs by ID or timestamp..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-slate-800 border-slate-700 text-white placeholder:text-slate-500"
          />
        </div>

        {/* Logs List */}
        {logs.length === 0 ? (
          <div className="py-12 text-center text-slate-500">
            <Database className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p className="font-medium">No logs loaded</p>
            <p className="text-sm">Click "Fetch Logs" to retrieve data from MongoDB</p>
          </div>
        ) : (
          <ScrollArea className="h-[400px]">
            <div className="space-y-3">
              {filteredLogs.map((log) => (
                <Card 
                  key={log._id}
                  className="bg-slate-800 border-slate-700 p-4 hover:bg-slate-750 hover:border-blue-600 transition-all cursor-pointer group"
                  onClick={() => {
                    onLoadLog(log.sessions);
                    toast.success(`Loaded ${log.sessionCount} sessions from log`);
                  }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-blue-400" />
                      <span className="text-white font-medium">{log.timestamp}</span>
                    </div>
                    <Badge variant="outline" className="border-slate-600 text-slate-300">
                      ID: {log._id}
                    </Badge>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-slate-400">Total Sessions</p>
                      <p className="text-white font-semibold text-lg">{log.sessionCount}</p>
                    </div>
                    <div>
                      <p className="text-slate-400">Anomalies Found</p>
                      <p className="text-red-400 font-semibold text-lg">{log.anomalyCount}</p>
                    </div>
                  </div>

                  <div className="mt-3 pt-3 border-t border-slate-700">
                    <p className="text-sm text-blue-400 group-hover:text-blue-300">
                      Click to load this log →
                    </p>
                  </div>
                </Card>
              ))}
            </div>
          </ScrollArea>
        )}

        {/* Connection Info */}
        <div className="mt-4 p-3 bg-slate-800 border border-slate-700 rounded-lg">
          <p className="text-xs text-slate-400">
            <span className="text-emerald-400 font-semibold">Backend Status:</span> http://localhost:8000
          </p>
          <p className="text-xs text-slate-500 mt-1">
            Connected to FastAPI + MongoDB
          </p>
        </div>
      </div>
    </Card>
  );
}
