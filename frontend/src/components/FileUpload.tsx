import { useRef, useState } from "react";
import { Button } from "./ui/button";
import { Upload, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { transformBackendAnomalyToSession } from "../lib/transformers";
import type { EVSession } from "./EVDashboard";

interface FileUploadProps {
  onFileUpload: (sessions: EVSession[]) => void;
}

export function FileUpload({ onFileUpload }: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      toast.error("Please upload a CSV file");
      return;
    }

    setIsUploading(true);
    
    try {
      // Call the backend API
      const response = await api.uploadAndPredict(file);
      
      // Transform backend anomalies to frontend sessions
      const sessions = response.anomalies.map(transformBackendAnomalyToSession);
      
      // Pass the transformed data to parent component
      onFileUpload(sessions);
      
      toast.success(
        `Analyzed ${response.total_sessions} sessions. Found ${response.anomalies_found} anomalies.`,
        {
          description: `File: ${response.filename}`,
          duration: 5000,
        }
      );
    } catch (error: any) {
      console.error('Upload error:', error);
      
      if (error.response) {
        // Backend returned an error
        toast.error(
          `Upload failed: ${error.response.data.detail || 'Server error'}`,
          { description: 'Please check your backend server is running on http://localhost:8000' }
        );
      } else if (error.request) {
        // Request made but no response
        toast.error(
          'Cannot connect to backend server',
          { description: 'Make sure your FastAPI server is running on http://localhost:8000' }
        );
      } else {
        // Something else happened
        toast.error('Upload failed', { description: error.message });
      }
    } finally {
      setIsUploading(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="hidden"
        disabled={isUploading}
      />
      <Button 
        onClick={() => fileInputRef.current?.click()}
        className="bg-blue-600 hover:bg-blue-700"
        disabled={isUploading}
      >
        {isUploading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Upload className="w-4 h-4 mr-2" />
            Upload CSV
          </>
        )}
      </Button>
    </>
  );
}