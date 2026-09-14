from unittest.mock import MagicMock, patch

from train_all import train_all


@patch("train_all.DataFetcher")
@patch("train_all.Backtester")
@patch("train_all.NIFTY50_SYMBOLS", ["TCS"])
def test_train_all_success(mock_backtester, mock_fetcher):
    mock_f_instance = MagicMock()

    mock_df = MagicMock()
    mock_df.empty = False

    mock_f_instance.fetch_daily_ohlcv.return_value = mock_df
    mock_f_instance.fetch_ohlcv.return_value = mock_df
    mock_f_instance.fetch_nifty_index.return_value = mock_df

    mock_fetcher.return_value = mock_f_instance

    mock_b_instance = MagicMock()
    mock_backtester.return_value = mock_b_instance

    train_all()

    assert mock_b_instance.run_backtest_for_symbol.called


@patch("train_all.DataFetcher")
@patch("train_all.Backtester")
@patch("train_all.NIFTY50_SYMBOLS", ["TCS"])
def test_train_all_no_data(mock_backtester, mock_fetcher):
    mock_f_instance = MagicMock()
    mock_f_instance.fetch_daily_ohlcv.return_value = None
    mock_f_instance.fetch_ohlcv.return_value = None
    mock_fetcher.return_value = mock_f_instance

    mock_b_instance = MagicMock()
    mock_backtester.return_value = mock_b_instance

    train_all()

    assert not mock_b_instance.run_backtest_for_symbol.called
