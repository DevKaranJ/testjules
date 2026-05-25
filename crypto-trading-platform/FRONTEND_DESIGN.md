# UI/UX Design & Architecture for Crypto Futures Quant Trading Platform

This document outlines the design and architecture for a professional-grade crypto futures trading workstation, covering both a Web Dashboard and a Terminal UI (TUI).

## 1. Full UI Architecture

### A. Web Application
- **Framework**: Next.js (App Router) + React.
- **Language**: TypeScript for strict typing of market data and configuration.
- **Styling**: Tailwind CSS configured for a deep dark, high-contrast theme.
- **State Management**: Zustand for global UI state, Redux Toolkit (RTK Query) for API caching, and specialized context providers for high-frequency WebSockets.
- **Visualizations**: Lightweight Charts (TradingView) for primary charts, D3.js + HTML5 Canvas for ultra-low latency order flow visualizations (Footprint, DOM heatmap).

### B. Terminal UI (TUI)
- **Framework**: Python Textual (or Rich for simpler scripts).
- **Architecture**: Async-first (using `asyncio`), matching the backend architecture.
- **Design Pattern**: Grid-based layout composed of modular widgets (Orderbook, Trades tape, Logs, Positions) connected via an internal pub/sub event bus linked to the core backend.

## 2. Web Dashboard Wireframes & Layout

**Grid-based dockable layout (inspired by Quantower & Hyperliquid)**

*   **Top Nav Bar**:
    *   Left: Logo, Workspace Selector (Default, Scalping, Research, Custom 1).
    *   Center: Current Symbol (BTC-PERP), Price, 24h Change, Volume.
    *   Right: Connections (🟢 API, 🟢 WS), Latency (e.g., 4ms), Portfolio Equity ($125,430), Risk Exposure bar, Settings Gear.
*   **Left Sidebar (Collapsed by default)**: Icons for Dashboard, Strategies, Backtesting, Paper Trading, Order Flow, Analytics, Logs.
*   **Center Workspace (Golden Layout / React-Grid-Layout)**:
    *   **Top Left (Large)**: Multi-timeframe Main Chart (Candlesticks + Indicators).
    *   **Bottom Left (Medium)**: Order Flow Footprint Chart + CVD.
    *   **Top Right (Narrow)**: Level 2 / Level 3 DOM Ladder with Heatmap.
    *   **Middle Right (Narrow)**: Tick-by-Tick Trade Tape (Aggression filtering).
    *   **Bottom Right (Medium)**: Strategy Monitor & Position Panel (Tabbed: Positions, Open Orders, Strategy Logs, Real-time PnL Curve).

## 3. Terminal UI (TUI) Layout

*   **Header**: `[Symbol: BTC-USDT] | [Price: 65,000] | [PnL: +$450.20] | [Mode: Live/Paper] | [Status: Running]`
*   **Main Grid**:
    *   **Left Panel (20%)**: Strategy Status (List of active strategies and current state/signals).
    *   **Center Panel (50%)**: Rolling Trade Tape + Basic ASCII/Braille Charting for Price Action.
    *   **Right Panel (30%)**: Condensed Order Book (Top 10 bids/asks with size bars).
*   **Bottom Panel (Split)**:
    *   **Top Half**: Active Positions (Side, Qty, Entry, Current Price, Unrealized PnL).
    *   **Bottom Half**: Structured Logs / Event Stream.
*   **Footer**: Keyboard Shortcuts (F1=Dashboard, F3=Positions, F4=DOM, Ctrl+C=Emergency Flatten).

## 4. Component Hierarchy (Web)

```
<App>
  <ThemeProvider>
    <WebSocketProvider>
      <StoreProvider>
        <TopNavBar />
        <Sidebar />
        <WorkspaceManager>
          <WidgetGrid>
            <ChartWidget />
            <OrderBookWidget>
               <DOMHeatmap />
               <DOMLadder />
            </OrderBookWidget>
            <TradeTapeWidget />
            <OrderFlowWidget>
               <FootprintChart />
               <CVDChart />
            </OrderFlowWidget>
            <ExecutionWidget>
               <StrategyMonitor />
               <PositionsTable />
               <OrderEntryForm />
            </ExecutionWidget>
          </WidgetGrid>
        </WorkspaceManager>
      </StoreProvider>
    </WebSocketProvider>
  </ThemeProvider>
</App>
```

## 5. State Management Design

1.  **Low-Frequency / REST Data** (Historical PnL, Strategy Configs, User Settings): Managed via **React Query (or RTK Query)**.
2.  **High-Frequency State** (Orderbook depth, Ticks): Managed outside of React's render cycle using **Refs** and custom Canvas renderers, or tightly scoped **Zustand** stores with shallow selectors to prevent re-renders of the entire dashboard.
3.  **UI Layout State** (Panel sizes, open tabs): Persisted to `localStorage` via Zustand.

## 6. Real-Time Data Flow

1.  **Backend** ingests exchange WS -> publishes to Redis Pub/Sub.
2.  **FastAPI WebSocket Server** subscribes to Redis -> broadcasts to connected Web clients via WebSockets.
3.  **Frontend WS Client** receives binary or compact JSON messages.
4.  **Web Worker (Frontend)** parses/deserializes data and routes updates to specific widget stores (e.g., merging Orderbook deltas).
5.  **Widgets** listen to their specific store selectors and update their canvas/DOM instantly.

## 7. WebSocket Architecture

-   **Multiplexed Connection**: A single WebSocket connection per client. The client sends subscription requests (e.g., `{"action": "subscribe", "channel": "orderbook_L2", "symbol": "BTCUSDT"}`).
-   **Data Serialization**: Use Protocol Buffers or MessagePack for high-frequency data to reduce bandwidth and parsing overhead.
-   **Heartbeats**: Ping/Pong every 10s to ensure connection vitality. Auto-reconnect with exponential backoff on failure.

## 8. Design System Specification

-   **Palette**:
    -   Backgrounds: Deep dark gray/blue (`#0a0e17`, `#111827`).
    -   Panels: Slightly lighter (`#1f2937`).
    -   Bullish/Buy: Vibrant Green (`#00E676`, `#10B981`).
    -   Bearish/Sell: High-visibility Red (`#FF5252`, `#EF4444`).
    -   Warning/Alerts: Amber (`#F59E0B`).
    -   Text: Primary (`#F3F4F6`), Secondary (`#9CA3AF`).
-   **Typography**:
    -   Headings/UI text: Inter or Roboto.
    -   Numbers/Monospace: JetBrains Mono or Fira Code (essential for aligning changing prices and quantities).
-   **Density**: High density. Professional traders prefer less padding and more information.

## 9. Suggested Frontend Libraries

-   **Core**: Next.js, React, TypeScript.
-   **Styling**: Tailwind CSS, Radix UI (for accessible unstyled primitives like dropdowns/tabs).
-   **Charting**: `lightweight-charts` (TradingView), `echarts` for complex multi-axis, `d3.js` for custom footprints.
-   **Layout**: `react-grid-layout` or `golden-layout`.
-   **State/Data**: Zustand, TanStack Query (React Query), `rxjs` (optional, for complex event streams).
-   **TUI**: `textual` (Python).

## 10. Folder Structure

```
crypto-trading-platform/
├── frontend/
│   ├── components/         # Reusable UI elements (Buttons, Tables, Tabs)
│   ├── widgets/            # Complex domain components (OrderBook, Chart, Tape)
│   ├── store/              # Zustand state definitions
│   ├── services/           # API and WebSocket clients, Web Workers
│   ├── types/              # TypeScript interfaces for market data/responses
│   ├── pages/              # Next.js routes (Dashboard, Backtest, Settings)
│   └── styles/             # Global CSS, Tailwind config
├── tui/
│   ├── app.py              # Textual App Entry Point
│   ├── components/         # TUI specific widgets (OrderBook, Positions, Tape)
│   └── theme.css           # Textual styling
```

## 11. Performance Optimization Plan

-   **Canvas vs DOM**: Render high-frequency updates (Orderbook heatmaps, fast charts, order flow) in HTML5 Canvas, strictly avoiding React DOM reconciliations.
-   **Web Workers**: Offload heavy computations (e.g., parsing WS data, calculating volume profiles, maintaining orderbook deltas) to Web Workers so the main UI thread never blocks.
-   **Throttling/Debouncing**: Throttle visual updates to 30-60 FPS (requestAnimationFrame) even if data arrives at 1000+ ticks/sec.
-   **Virtualization**: Use `react-window` or `react-virtuoso` for the Trade Tape and Log windows to only render visible rows.

## 12. Mobile Responsiveness Strategy

While power-user quant dashboards are inherently desktop-first:
-   **Mobile View**: Strip down to a single-column view. Top chart, followed by condensed position summary, then simplified order execution.
-   Disable heavy Canvas visualizations (Footprint, DOM heatmap) on mobile to save battery and ensure performance.

## 13. Multi-Monitor Workflow Design

-   **Detachable Panels**: Implement a system (via Browser Window API) where widgets can be popped out into their own standalone browser windows.
-   **Sync via LocalStorage/BroadcastChannel**: When a user changes the symbol in the main window, it broadcasts the change to all popped-out windows (e.g., updating the standalone order book window instantly).

## 14. UX Recommendations for Traders

-   **One-Click Execution**: For manual/paper trading, support "click to trade" directly on the DOM/Chart.
-   **Visual Noise Reduction**: Provide toggles to hide decimals for high-priced assets, or group orderbook levels to reduce flicker.
-   **Focus on Exceptions**: Strategy monitors should heavily highlight errors, rejections, or unexpected liquidations over normal running logs.

## 15. Suggested Animations/Interactions

-   **Minimal Animations**: Avoid long transitions. Hover states should be instantaneous (0-50ms).
-   **Flash Indicators**: When a large market order hits the tape, briefly flash the row or DOM level background color, fading out over 300ms.
-   **Smooth Scrolling**: Trade tapes should auto-scroll smoothly but allow pausing when hovered over.

## 16. Theme System

-   Support deep customization via CSS variables (`--bg-primary`, `--up-color`, `--down-color`).
-   Allow users to import/export theme JSON files. Include a "High Contrast" mode for visually impaired users and an "OLED" pure black mode.

## 17. Plugin/Widget Architecture

-   Design the layout engine to accept dynamic components.
-   A widget is registered with a manifest: `{ id: 'custom_indicator', name: 'My Alpha', component: DynamicReactComponent, defaultSize: [w, h] }`.
-   This allows future strategies to inject their own custom visualization panels into the main dashboard without hardcoding them into the core app.
