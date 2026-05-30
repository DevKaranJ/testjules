'use client';

import LiveTradeFeed from '@/components/LiveTradeFeed';
import ChartWidget from '@/components/ChartWidget';
import StrategyControlPanel from '@/components/StrategyControlPanel';

export default function Home() {
  return <Dashboard />;
}

function Dashboard() {
  return (
    <main className="min-h-screen">
      <div className="terminal-grid">
        <div className="col-span-2 flex flex-col gap-2">
          <ChartWidget />
          <LiveTradeFeed />
        </div>
        <div className="col-span-1">
          <StrategyControlPanel />
        </div>
      </div>
    </main>
  );
}
