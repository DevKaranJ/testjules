from pydantic import BaseModel, Field
from typing import Optional


class MeanReversionConfig(BaseModel):
    deviation: float = Field(default=2.0, ge=0.5, le=5.0, description="Z-score deviation threshold")
    lookback: int = Field(default=20, ge=5, le=100, description="Lookback window for returns")


class KalmanPairsConfig(BaseModel):
    z_score_threshold: float = Field(default=2.0, ge=0.5, le=4.0, description="Z-score entry threshold")
    lookback: int = Field(default=100, ge=10, le=500, description="Price history window")


class HMMRegimeConfig(BaseModel):
    n_states: int = Field(default=3, ge=2, le=5, description="Number of hidden states")
    lookback: int = Field(default=50, ge=10, le=200, description="Lookback window")


class IVCrushConfig(BaseModel):
    iv_percentile_threshold: float = Field(default=75.0, ge=50.0, le=99.0, description="IV percentile entry threshold")
    lookback: int = Field(default=30, ge=10, le=100, description="Volatility lookback")


class OrderFlowScalpingConfig(BaseModel):
    bid_ask_spread_threshold: float = Field(default=0.5, ge=0.1, le=5.0, description="Spread threshold in bps")
    min_volume: int = Field(default=10, ge=1, le=1000, description="Minimum volume for entry")


class DispersionArbConfig(BaseModel):
    z_score_entry: float = Field(default=2.0, ge=0.5, le=4.0, description="Z-score entry threshold")
    lookback: int = Field(default=20, ge=5, le=100, description="Returns lookback")


class PCANeutralConfig(BaseModel):
    n_components: int = Field(default=3, ge=1, le=10, description="Number of PCA components")
    hedging_ratio: float = Field(default=1.0, ge=0.1, le=3.0, description="Hedge ratio")
    lookback: int = Field(default=50, ge=10, le=200, description="Lookback for PCA fitting")


class VPINToxicityConfig(BaseModel):
    vpin_threshold: float = Field(default=2.0, ge=0.5, le=5.0, description="VPIN z-score threshold")
    lookback: int = Field(default=50, ge=10, le=200, description="Volume imbalance lookback")


STRATEGY_CONFIG_MAP = {
    "MeanReversion": MeanReversionConfig,
    "KalmanPairs": KalmanPairsConfig,
    "HMMRegime": HMMRegimeConfig,
    "IVCrush": IVCrushConfig,
    "OrderFlowScalping": OrderFlowScalpingConfig,
    "DispersionArb": DispersionArbConfig,
    "PCANeutral": PCANeutralConfig,
    "VPINToxicity": VPINToxicityConfig,
}
