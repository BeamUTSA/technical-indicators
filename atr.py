import pandas as pd
from core.load_data import load_or_update

def average_true_range(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = data.copy()

    high = df['2. high']
    low = df['3. low']
    close = df['4. close']

    df['H-L'] = high - low
    df['H-C'] = (high - close.shift()).abs()
    df['L-C'] = (low - close.shift()).abs()

    df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()

    return df

def run(ticker: str, return_data: bool = False, period: int = 14):
    """Wrapper for GUI/CLI use."""
    df = load_or_update(ticker)
    df = average_true_range(df, period)

    last_atr = df["ATR"].iloc[-1]
    average_atr = df["ATR"].mean()

    # Basic interpretation: ATR above average means increased volatility
    if last_atr > average_atr:
        volatility = "high"
    else:
        volatility = "low"

    if return_data:
        return volatility, df
    return volatility
