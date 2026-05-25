'use client';

import { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

import { useStore } from '@/store/useStore';
import { ISeriesApi } from 'lightweight-charts';

export default function ChartWidget() {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const latestPrice = useStore(state => state.prices['BTC/USDT']);
  const seriesRef = useRef<ISeriesApi<"Line"> | null>(null);

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
    seriesRef.current = lineSeries;

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

  // Update chart when live price comes in
  useEffect(() => {
      if (seriesRef.current && latestPrice) {
          // Lightweight-charts requires strictly increasing time (unix timestamp in seconds)
          const unixTime = Math.floor(Date.now() / 1000);

          seriesRef.current.update({
              time: unixTime as any,
              value: latestPrice
          });
      }
  }, [latestPrice]);

  return (
    <div className="w-full relative">
        {latestPrice && (
            <div className="absolute top-2 left-2 z-10 text-white font-mono bg-black bg-opacity-50 px-2 py-1 rounded">
                Live BTC: ${latestPrice.toFixed(2)}
            </div>
        )}
        <div ref={chartContainerRef} className="w-full h-[400px]" />
    </div>
  );
}
