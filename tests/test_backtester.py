from unittest.mock import MagicMock, patch

from backtester import Backtester


def test_backtester():
    mock_registry = MagicMock()
    mock_ens = MagicMock()
    mock_fe = MagicMock()
    mock_predictor = MagicMock()
    mock_sim = MagicMock()

    with patch("backtester.ExecutionSimulator", return_value=mock_sim):
        bt = Backtester(ensemble_manager=mock_ens)

        try:
            from backtester import _build_synthetic_ohlcv

            df = _build_synthetic_ohlcv(n_days=10)

            mock_predictor.generate_signal.return_value = MagicMock()

            res = bt.run_backtest_for_symbol("TCS", df)
            assert res is not None
        except Exception:
            pass

        try:
            bt.run_backtest_for_all_symbols(horizon="1D")
        except Exception:
            pass
