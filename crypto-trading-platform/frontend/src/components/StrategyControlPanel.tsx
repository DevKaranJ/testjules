'use client';

export default function StrategyControlPanel() {
  return (
    <div className="bg-gray-900 p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-white">Strategy Control Panel</h2>
      <div className="space-y-4">

        <div className="flex justify-between items-center border-b border-gray-800 pb-2">
            <span className="text-gray-300">Kalman Filter Pairs</span>
            <button className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-500">Run</button>
        </div>

        <div className="flex justify-between items-center border-b border-gray-800 pb-2">
            <span className="text-gray-300">VPIN Toxicity Model</span>
            <button className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-500">Stop</button>
        </div>

        <div className="flex justify-between items-center border-b border-gray-800 pb-2">
            <span className="text-gray-300">Order Flow Scalping</span>
            <button className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-500">Run</button>
        </div>

      </div>
    </div>
  );
}
