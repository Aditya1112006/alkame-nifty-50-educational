from unittest.mock import MagicMock, patch

import pandas as pd

from predictor import PredictionSignal
from scalping import ScalpingEngine


def test_scalping_engine_find_opportunities():
    mock_predictor = MagicMock()
    mock_data_fetcher = MagicMock()
    mock_feature_engineer = MagicMock()

    # Mock stock data
    df = pd.DataFrame(
        {
            "Close": [100.0, 101.0, 102.0],
            "High": [101.0, 102.0, 103.0],
            "Low": [99.0, 100.0, 101.0],
            "Volume": [100, 200, 300],
            "ATR_14": [1.0, 1.0, 1.0],
        }
    )
    mock_data_fetcher.fetch_ohlcv.return_value = df
    mock_data_fetcher.check_staleness.return_value = False

    # Mock features
    mock_feature_engineer.engineer_features_for_horizon.return_value = df

    # Mock signal
    mock_sig = PredictionSignal(
        timestamp="2026-01-01T00:00:00",
        symbol="TCS",
        horizon="1D",
        action="BUY",
        model_predicted_class="BUY",
        raw_confidence=0.8,
        calibrated_confidence=0.8,
        target_price=110.0,
        stop_loss=90.0,
        suppressed=False,
        model_version="1.0",
        feature_version="1.0",
        risk_adjusted_confidence=0.8,
        agreement_fraction=1.0,
        downside_summary=[],
        upside_summary=[],
        is_safe_to_trade_live=True,
    )

    mock_predictor.generate_signal.return_value = mock_sig

    engine = ScalpingEngine(mock_predictor, mock_data_fetcher, mock_feature_engineer)

    with patch("scalping.NIFTY50_SYMBOLS", ["TCS"]):
        setups = engine.find_opportunities()
        assert len(setups) == 1
        assert setups[0].symbol == "TCS"
        assert setups[0].action == "BUY"
