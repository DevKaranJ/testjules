'use client';

import { useState } from 'react';

interface ParamDef {
  name: string;
  label: string;
  default: number;
  min: number;
  max: number;
  step: number;
}

const STRATEGY_PARAMS: Record<string, ParamDef[]> = {
  KalmanPairs: [
    { name: 'z_score_threshold', label: 'Z-Score Threshold', default: 2.0, min: 0.5, max: 4.0, step: 0.1 },
    { name: 'lookback', label: 'Lookback', default: 100, min: 10, max: 500, step: 10 },
  ],
  MeanReversion: [
    { name: 'deviation', label: 'Deviation Threshold', default: 2.0, min: 0.5, max: 5.0, step: 0.1 },
    { name: 'lookback', label: 'Lookback', default: 20, min: 5, max: 100, step: 5 },
  ],
  HMMRegime: [
    { name: 'n_states', label: 'Hidden States', default: 3, min: 2, max: 5, step: 1 },
    { name: 'lookback', label: 'Lookback', default: 50, min: 10, max: 200, step: 10 },
  ],
};

interface Props {
  strategyName: string;
  onClose: () => void;
}

export default function StrategyConfigPanel({ strategyName, onClose }: Props) {
  const params = STRATEGY_PARAMS[strategyName] ?? [];
  const [values, setValues] = useState<Record<string, number>>(() => {
    const initial: Record<string, number> = {};
    for (const p of params) initial[p.name] = p.default;
    return initial;
  });
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-[#111] border border-[#1f1f1f] p-5 w-full max-w-sm mx-4" onClick={(e) => e.stopPropagation()}>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm uppercase tracking-wider" style={{color: '#4ade80'}}>
            {strategyName.replace(/([A-Z])/g, ' $1').trim()}
          </h3>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-lg leading-none">&times;</button>
        </div>

        {params.length === 0 ? (
          <p className="text-gray-600 text-xs">No configurable parameters.</p>
        ) : (
          <div className="space-y-4">
            {params.map((p) => (
              <div key={p.name}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-500">{p.label}</span>
                  <span className="text-white font-mono">{values[p.name]?.toFixed(p.step < 1 ? 1 : 0)}</span>
                </div>
                <input
                  type="range"
                  min={p.min}
                  max={p.max}
                  step={p.step}
                  value={values[p.name] ?? p.default}
                  onChange={(e) => setValues((v) => ({ ...v, [p.name]: parseFloat(e.target.value) }))}
                  className="terminal-slider w-full"
                />
              </div>
            ))}
          </div>
        )}

        {params.length > 0 && (
          <button
            onClick={handleSave}
            className="terminal-btn buy w-full mt-4 text-center"
          >
            {saved ? 'SAVED' : 'SAVE PARAMETERS'}
          </button>
        )}
      </div>
    </div>
  );
}
