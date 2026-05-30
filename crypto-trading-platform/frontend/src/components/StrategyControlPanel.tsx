'use client';

import { useState, useEffect } from 'react';
import StrategyConfigPanel from './StrategyConfigPanel';

interface StrategyStatus {
  [name: string]: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const STRATEGY_NAMES = [
  'KalmanPairs',
  'VPINToxicity',
  'OrderFlowScalping',
  'MeanReversion',
  'HMMRegime',
  'IVCrush',
  'DispersionArb',
  'PCANeutral',
];

export default function StrategyControlPanel() {
  const [statuses, setStatuses] = useState<StrategyStatus>({});
  const [configFor, setConfigFor] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/strategies`)
      .then((r) => r.json())
      .then((data) => setStatuses(data.strategies || data))
      .catch(() => {});
  }, []);

  const toggle = async (name: string, current: string) => {
    const action = current === 'running' ? 'stop' : 'run';
    try {
      const res = await fetch(`${API_BASE}/api/strategies/${name}/${action}`, { method: 'POST' });
      const data = await res.json();
      setStatuses((prev) => ({ ...prev, [name]: data.status }));
    } catch {
      // offline
    }
  };

  return (
    <>
      <div className="terminal-panel">
        <div className="terminal-header">
          <span className="title">Strategy Control Panel</span>
        </div>
        <div className="p-2">
          {STRATEGY_NAMES.map((name) => {
            const status = statuses[name] || 'stopped';
            const isRunning = status === 'running';
            return (
              <div key={name} className="flex justify-between items-center py-1.5 border-b border-[#1f1f1f]">
                <span className="text-gray-400 text-xs truncate mr-2">{name.replace(/([A-Z])/g, ' $1').trim()}</span>
                <div className="flex gap-1 shrink-0">
                  <button
                    onClick={() => setConfigFor(name)}
                    className="terminal-btn"
                    title="Configure"
                  >
                    Config
                  </button>
                  <button
                    onClick={() => toggle(name, status)}
                    className={`terminal-btn ${isRunning ? 'sell' : 'buy'}`}
                  >
                    {isRunning ? 'Stop' : 'Run'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {configFor && <StrategyConfigPanel strategyName={configFor} onClose={() => setConfigFor(null)} />}
    </>
  );
}
