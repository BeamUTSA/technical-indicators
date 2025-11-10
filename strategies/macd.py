import pandas as pd
from core.load_data import load_or_update

def macd(data: pd.DataFrame, short_period: int = 12, long_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
    df = data.copy()
    close = df['4. close']

    df['EMA_short'] = close.ewm(span=short_period, adjust=False).mean()
    df['EMA_long'] = close.ewm(span=long_period, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()

    df['Histogram'] = df['MACD'] - df['Signal']
    return df

def run(ticker: str, return_data: bool = False, short: int = 12, long: int = 26, signal: int = 9):
    """Wrapper for GUI/CLI use."""
    df = load_or_update(ticker)
    df = macd(df, short, long, signal)

    last_macd = df["MACD"].iloc[-1]
    last_signal = df["Signal"].iloc[-1]

    if last_macd > last_signal:
        outcome = "bullish"
    elif last_macd < last_signal:
        outcome = "bearish"
    else:
        outcome = "hold"

    if return_data:
        return outcome, df
    return outcome
