'use client';

import { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

export default function ChartWidget() {
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#111827' },
        textColor: '#D1D5DB',
      },
      grid: {
        vertLines: { color: '#1F2937' },
        horzLines: { color: '#1F2937' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 400,
    });

    // lightweight-charts changed their API. We need `addSeries` with `LineSeries`
    const lineSeries = chart.addLineSeries({ color: '#10B981' });
    lineSeries.setData([
      { time: '2024-01-01', value: 60000 },
      { time: '2024-01-02', value: 61000 },
      { time: '2024-01-03', value: 60500 },
      { time: '2024-01-04', value: 62000 },
      { time: '2024-01-05', value: 63500 },
    ]);

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  return <div ref={chartContainerRef} className="w-full h-[400px]" />;
}
