{/* # /frontend/src/components/MLDashboard.jsx */}

import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, Download, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

export const MLDashboard = ({ onError }) => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await api.get('/metrics');
      if (response.data && response.data.length > 0) {
        setMetrics(response.data[0]);
      }
    } catch (error) {
      onError(error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      await api.post('/upload-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      await fetchMetrics();
    } catch (error) {
      onError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleExportData = async () => {
    try {
      const response = await api.get('/export-csv', {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'tenis_match_data.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      onError(error);
    }
  };

  const handleTrainModel = async () => {
    setLoading(true);
    try {
      const response = await api.post('/train');
      setMetrics(response.data);
    } catch (error) {
      onError(error);
    } finally {
      setLoading(false);
    }
  };

  if (!metrics) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Carregando métricas...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Actions */}
      <div className="flex gap-4">
        <Button 
          onClick={() => document.getElementById('fileUpload').click()}
          disabled={loading}
        >
          <Upload className="mr-2 h-4 w-4" />
          Importar CSV
        </Button>
        <input
          id="fileUpload"
          type="file"
          accept=".csv"
          className="hidden"
          onChange={handleFileUpload}
        />
        
        <Button 
          onClick={handleExportData}
          disabled={loading}
        >
          <Download className="mr-2 h-4 w-4" />
          Exportar CSV
        </Button>
        
        <Button 
          onClick={handleTrainModel}
          disabled={loading}
          variant="secondary"
        >
          <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Treinar Modelo
        </Button>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Métricas do Modelo</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <p className="text-sm text-gray-500">Acurácia</p>
                <p className="text-2xl font-bold">
                  {(metrics.accuracy * 100).toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-500">Precisão</p>
                <p className="text-2xl font-bold">
                  {(metrics.precision * 100).toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-500">Recall</p>
                <p className="text-2xl font-bold">
                  {(metrics.recall * 100).toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-500">F1-Score</p>
                <p className="text-2xl font-bold">
                  {(metrics.f1_score * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Matriz de Confusão</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={metrics.confusion_matrix}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar 
                  dataKey="actual_positive" 
                  fill="#22c55e" 
                  name="Positivo Real" 
                />
                <Bar 
                  dataKey="actual_negative" 
                  fill="#ef4444" 
                  name="Negativo Real" 
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* ROC Curve */}
      <Card>
        <CardHeader>
          <CardTitle>Curva ROC</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics.roc_curve_data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="fpr" 
                label={{ 
                  value: 'Taxa de Falsos Positivos', 
                  position: 'bottom' 
                }} 
              />
              <YAxis 
                label={{ 
                  value: 'Taxa de Verdadeiros Positivos', 
                  angle: -90, 
                  position: 'left' 
                }} 
              />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="tpr" 
                stroke="#3b82f6" 
                strokeWidth={2} 
                dot={false} 
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};