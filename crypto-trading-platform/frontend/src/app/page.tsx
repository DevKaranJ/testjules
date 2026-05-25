import PositionTable from '@/components/PositionTable';
import ChartWidget from '@/components/ChartWidget';
import StrategyControlPanel from '@/components/StrategyControlPanel';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col p-8 bg-black text-white">
      <h1 className="text-3xl font-bold mb-8">Crypto Quant Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="col-span-1 lg:col-span-2 bg-gray-900 rounded-lg p-4 border border-gray-800">
            <ChartWidget />
        </div>

        <div className="col-span-1 flex flex-col gap-6">
          <StrategyControlPanel />
          <PositionTable />
        </div>
      </div>
    </main>
  );
}
