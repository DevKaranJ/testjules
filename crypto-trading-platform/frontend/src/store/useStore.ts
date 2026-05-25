import { create } from 'zustand'

interface Trade {
  strategy: string;
  symbol: string;
  pnl: number;
}

interface PlatformState {
  trades: Trade[];
  prices: Record<string, number>;
  addTrade: (trade: Trade) => void;
  updatePrice: (symbol: string, price: number) => void;
}

export const useStore = create<PlatformState>((set) => ({
  trades: [
    { strategy: 'KalmanPairs', symbol: 'BTC/USDT', pnl: 150 },
    { strategy: 'OrderFlow', symbol: 'ETH/USDT', pnl: -20 },
  ],
  prices: {},
  addTrade: (trade) => set((state) => ({ trades: [...state.trades, trade] })),
  updatePrice: (symbol, price) => set((state) => ({
    prices: { ...state.prices, [symbol]: price }
  })),
}))

// Simple websocket wiring
if (typeof window !== 'undefined') {
  const wsUrl = process.env.NEXT_PUBLIC_API_URL
    ? process.env.NEXT_PUBLIC_API_URL.replace('http', 'ws') + '/ws/market_data'
    : 'ws://localhost:8000/ws/market_data';

  const ws = new WebSocket(wsUrl);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'orderbook_update') {
        const midPrice = (data.best_bid + data.best_ask) / 2;
        useStore.getState().updatePrice(data.symbol, midPrice);
      }
    } catch (e) {
      console.log('Error parsing WS message', e);
    }
  };
}
