import { create } from 'zustand'

interface Trade {
  strategy: string;
  symbol: string;
  pnl: number;
}

interface PlatformState {
  trades: Trade[];
  addTrade: (trade: Trade) => void;
}

export const useStore = create<PlatformState>((set) => ({
  trades: [
    { strategy: 'KalmanPairs', symbol: 'BTC/USDT', pnl: 150 },
    { strategy: 'OrderFlow', symbol: 'ETH/USDT', pnl: -20 },
  ],
  addTrade: (trade) => set((state) => ({ trades: [...state.trades, trade] })),
}))
