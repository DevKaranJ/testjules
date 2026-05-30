import { create } from 'zustand'

interface Trade {
  id?: number;
  strategy: string;
  symbol: string;
  direction?: string;
  entry_price?: number;
  exit_price?: number;
  quantity?: number;
  pnl: number;
  fee?: number;
  timestamp?: string;
}

interface PlatformState {
  trades: Trade[];
  prices: Record<string, number>;
  addTrade: (trade: Trade) => void;
  updatePrice: (symbol: string, price: number) => void;
}

export const useStore = create<PlatformState>((set) => ({
  trades: [],
  prices: {},
  addTrade: (trade) => set((state) => ({
    trades: [trade, ...state.trades].slice(0, 50),
  })),
  updatePrice: (symbol, price) => set((state) => ({
    prices: { ...state.prices, [symbol]: price }
  })),
}))

// WebSocket with auto-reconnect
if (typeof window !== 'undefined') {
  const wsUrl = process.env.NEXT_PUBLIC_API_URL
    ? process.env.NEXT_PUBLIC_API_URL.replace('http', 'ws') + '/ws/market_data'
    : 'ws://localhost:8000/ws/market_data';

  let ws: WebSocket | null = null;
  let reconnectAttempts = 0;

  function connect() {
    ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'orderbook_update') {
          const midPrice = (data.best_bid + data.best_ask) / 2;
          useStore.getState().updatePrice(data.symbol, midPrice);
        }
        if (data.type === 'trade_executed') {
          useStore.getState().addTrade({
            strategy: data.strategy,
            symbol: data.symbol,
            direction: data.direction,
            entry_price: data.entry_price,
            pnl: data.pnl,
            timestamp: data.timestamp,
          });
        }
      } catch (e) {
        console.log('Error parsing WS message', e);
      }
    };

    ws.onclose = () => {
      reconnectAttempts++;
      const delay = Math.min(3000 * Math.pow(1.5, reconnectAttempts), 30000);
      setTimeout(connect, delay);
    };

    ws.onerror = () => {
      ws?.close();
    };

    ws.onopen = () => {
      reconnectAttempts = 0;
    };
  }

  connect();
}
