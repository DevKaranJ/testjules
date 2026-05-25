'use client';

import { useStore } from '@/store/useStore';

export default function PositionTable() {
  const trades = useStore((state) => state.trades);

  return (
    <div className="bg-gray-900 p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-white">Active Positions</h2>
      <table className="w-full text-left text-gray-300">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="py-2">Strategy</th>
            <th className="py-2">Symbol</th>
            <th className="py-2">PnL</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((trade, idx) => (
            <tr key={idx} className="border-b border-gray-800">
              <td className="py-2">{trade.strategy}</td>
              <td className="py-2">{trade.symbol}</td>
              <td className={`py-2 ${trade.pnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                ${trade.pnl}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
