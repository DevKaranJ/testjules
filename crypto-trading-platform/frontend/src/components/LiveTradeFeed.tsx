'use client';

import { useStore } from '@/store/useStore';

export default function LiveTradeFeed() {
  const trades = useStore((state) => state.trades);

  return (
    <div className="terminal-panel">
      <div className="terminal-header">
        <span className="title">Trade Feed</span>
        <span className="text-xs text-gray-600">{trades.length} trades</span>
      </div>
      {trades.length === 0 ? (
        <div className="p-4 text-center text-gray-600 text-xs">
          No trades yet — waiting for signals...
        </div>
      ) : (
        <div className="max-h-52 overflow-y-auto">
          <table className="terminal-table">
            <thead>
              <tr>
                <th>Strategy</th>
                <th>Sym</th>
                <th>Dir</th>
                <th className="text-right">PnL</th>
                <th className="text-right">Entry</th>
              </tr>
            </thead>
            <tbody>
              {trades.slice(0, 30).map((trade, idx) => (
                <tr key={trade.id ?? idx}>
                  <td style={{maxWidth: 100}} className="truncate">{trade.strategy}</td>
                  <td>{trade.symbol}</td>
                  <td>
                    <span style={{color: trade.direction === 'LONG' ? '#4ade80' : '#ef4444'}}>
                      {trade.direction === 'LONG' ? '▲' : trade.direction === 'SHORT' ? '▼' : ''}
                    </span>
                  </td>
                  <td className="text-right" style={{color: trade.pnl >= 0 ? '#4ade80' : '#ef4444'}}>
                    {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                  </td>
                  <td className="text-right text-gray-600">
                    ${trade.entry_price?.toFixed(2) ?? ''}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
