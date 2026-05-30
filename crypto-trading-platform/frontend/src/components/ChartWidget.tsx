'use client';

import { useEffect, useRef } from 'react';
import { createChart, type ISeriesApi, type UTCTimestamp } from 'lightweight-charts';

import { useStore } from '@/store/useStore';

export default function ChartWidget() {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const latestPrice = useStore(state => state.prices['BTC/USDT']);
  const seriesRef = useRef<ISeriesApi<"Line"> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#0a0a0a' },
        textColor: '#808080',
      },
      grid: {
        vertLines: { color: '#1a1a1a' },
        horzLines: { color: '#1a1a1a' },
      },
      crosshair: {
        vertLine: { color: '#4ade80', style: 2, width: 1, labelBackgroundColor: '#4ade80' },
        horzLine: { color: '#4ade80', style: 2, width: 1, labelBackgroundColor: '#4ade80' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 350,
      handleScroll: false,
      handleScale: false,
    });

    const lineSeries = chart.addLineSeries({
      color: '#4ade80',
      lineWidth: 1,
      priceLineVisible: false,
    });
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

  useEffect(() => {
      if (seriesRef.current && latestPrice) {
          const unixTime = Math.floor(Date.now() / 1000);
          seriesRef.current.update({
              time: unixTime as UTCTimestamp,
              value: latestPrice
          });
      }
  }, [latestPrice]);

  return (
    <div className="terminal-panel w-full relative">
      <div className="terminal-header">
        <span className="title">BTC/USDT</span>
        <div className="flex items-center gap-3">
          {latestPrice && (
            <span className="text-sm font-bold" style={{color: '#4ade80'}}>
              ${latestPrice.toFixed(2)}
            </span>
          )}
          <span className="text-xs text-gray-600">1D · CANDLES · M5</span>
        </div>
      </div>
      <div ref={chartContainerRef} className="w-full h-[350px]" />
    </div>
  );
}
