// /frontend/src/components/MetricsCard.jsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { cn } from '@/lib/utils';
import { TrendingUp, TrendingDown } from 'lucide-react';

const MetricDisplay = ({ label, value, previousValue, format, className }) => {
  const change = previousValue
    ? ((value - previousValue) / previousValue) * 100
    : 0;
  const isPositive = change >= 0;

  return (
    <div className={cn('space-y-2', className)}>
      <p className="text-sm text-muted-foreground">{label}</p>
      <div className="flex items-baseline space-x-2">
        <p className="text-2xl font-semibold">
          {typeof format === 'function' ? format(value) : value}
        </p>
        {previousValue && (
          <div
            className={cn(
              'flex items-center text-sm',
              isPositive ? 'text-green-600' : 'text-red-600'
            )}
          >
            {isPositive ? (
              <TrendingUp className="mr-1 h-4 w-4" />
            ) : (
              <TrendingDown className="mr-1 h-4 w-4" />
            )}
            {Math.abs(change).toFixed(1)}%
          </div>
        )}
      </div>
    </div>
  );
};

export const MetricsCard = ({
  title,
  metrics = [],
  className,
  gridCols = 2,
}) => {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div
          className={cn('grid gap-4', {
            'grid-cols-1': gridCols === 1,
            'grid-cols-2': gridCols === 2,
            'grid-cols-3': gridCols === 3,
            'grid-cols-4': gridCols === 4,
          })}
        >
          {metrics.map((metric, index) => (
            <MetricDisplay
              key={index}
              label={metric.label}
              value={metric.value}
              previousValue={metric.previousValue}
              format={metric.format}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

// Exemplo de uso:
export const ModelMetricsCard = ({ 
  accuracy, 
  precision, 
  recall, 
  f1Score,
  previousMetrics = null 
}) => {
  const formatPercent = (value) => `${(value * 100).toFixed(1)}%`;

  const metrics = [
    {
      label: 'Acurácia',
      value: accuracy,
      previousValue: previousMetrics?.accuracy,
      format: formatPercent,
    },
    {
      label: 'Precisão',
      value: precision,
      previousValue: previousMetrics?.precision,
      format: formatPercent,
    },
    {
      label: 'Recall',
      value: recall,
      previousValue: previousMetrics?.recall,
      format: formatPercent,
    },
    {
      label: 'F1-Score',
      value: f1Score,
      previousValue: previousMetrics?.f1Score,
      format: formatPercent,
    },
  ];

  return (
    <MetricsCard
      title="Métricas do Modelo"
      metrics={metrics}
      gridCols={2}
    />
  );
};