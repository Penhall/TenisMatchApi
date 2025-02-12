{/* # /frontend/src/App.jsx */}

import React from 'react';
import { MLDashboard } from './components/MLDashboard';
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle } from 'lucide-react';

const App = () => {
  const [error, setError] = React.useState(null);

  const handleError = (error) => {
    setError(error.message);
    setTimeout(() => setError(null), 5000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            TenisMatch - Dashboard ML
          </h1>
        </div>
      </header>

      {/* Error Alert */}
      {error && (
        <div className="max-w-7xl mx-auto mt-4 px-4">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {error}
            </AlertDescription>
          </Alert>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <MLDashboard onError={handleError} />
      </main>

      {/* Footer */}
      <footer className="bg-white shadow mt-8">
        <div className="max-w-7xl mx-auto py-4 px-4 text-center text-gray-600">
          <p>TenisMatch - Sistema de Recomendação de Tênis usando Machine Learning</p>
        </div>
      </footer>
    </div>
  );
};

export default App;