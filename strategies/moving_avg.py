import pandas as pd
from core.load_data import load_or_update


def moving_average_crossover(data: pd.DataFrame, short=20, long=50) -> pd.DataFrame:
    """Original function (kept for reuse in CLI/backtesting)."""
    df = data.copy()
    df["Close"] = df["4. close"].astype(float)
    df["SMA_short"] = df["Close"].rolling(window=short).mean()
    df["SMA_long"] = df["Close"].rolling(window=long).mean()
    df["Signal"] = 0
    df.loc[df["SMA_short"] > df["SMA_long"], "Signal"] = 1
    df.loc[df["SMA_short"] < df["SMA_long"], "Signal"] = -1
    return df


def run(ticker: str, return_data: bool = False):
    """Wrapper for GUI/CLI menu integration."""
    df = load_or_update(ticker)
    df = moving_average_crossover(df)

    # Translate last signal into bullish/bearish/hold
    last_signal = df["Signal"].iloc[-1]
    if last_signal == 1:
        signal = "bullish"
    elif last_signal == -1:
        signal = "bearish"
    else:
        signal = "hold"

    if return_data:
        return signal, df
    return signal
