from .base import Strategy
from typing import Dict, Any
import numpy as np

class HMMRegimeStrategy(Strategy):
    """
    5. Hidden Markov Regime Detection
    Categorizes the market into distinct structural states using Gaussian emissions
    and a simplified Viterbi inference algorithm.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.lookback = self.config.get("lookback", 50)
        self.n_states = self.config.get("n_states", 3)
        self.prices = []
        self.returns = []
        self.transmat = np.ones((self.n_states, self.n_states)) * 0.1
        np.fill_diagonal(self.transmat, 0.8)
        self.means = np.array([-0.001, 0.0, 0.001])
        self.stds = np.array([0.02, 0.005, 0.02])
        self.state_labels = ["LowVol_Range", "HighVol_Bull", "HighVol_Bear"]

    def on_tick(self, tick_data: Dict[str, Any]) -> None:
        self.prices.append(tick_data["price"])
        if len(self.prices) > self.lookback:
            self.prices.pop(0)
        if len(self.prices) >= 2:
            ret = (self.prices[-1] - self.prices[-2]) / self.prices[-2]
            self.returns.append(ret)
            if len(self.returns) > self.lookback:
                self.returns.pop(0)

    def on_orderbook(self, orderbook_data: Dict[str, Any]) -> None:
        pass

    def _viterbi(self, obs: np.ndarray) -> int:
        """Infer most likely state using forward algorithm."""
        if len(obs) == 0:
            return 1
        delta = np.ones(self.n_states) / self.n_states
        for t in range(len(obs)):
            likelihood = np.array([
                np.exp(-0.5 * ((obs[t] - self.means[s]) / self.stds[s]) ** 2)
                / (self.stds[s] * np.sqrt(2 * np.pi))
                for s in range(self.n_states)
            ])
            delta = delta @ self.transmat * likelihood
            s = delta.sum()
            if s > 0:
                delta /= s
        return int(np.argmax(delta))

    def generate_signal(self) -> Any:
        if len(self.returns) < 10:
            return "NO TRADE — insufficient history for regime detection."

        obs = np.array(self.returns[-20:])
        state = self._viterbi(obs)

        for s in range(self.n_states):
            mask = np.array([self._viterbi(np.array([r])) == s for r in self.returns[-50:]])
            subset = np.array(self.returns[-50:])[mask]
            if len(subset) > 0:
                self.means[s] = np.mean(subset)
                self.stds[s] = max(np.std(subset), 1e-6)

        return "NO TRADE — meta-strategy, market state: " + self.state_labels[state]
