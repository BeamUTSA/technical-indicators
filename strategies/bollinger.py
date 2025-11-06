import pandas as pd
from core.load_data import load_or_update

def bollinger_bands(data: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df = data.copy()
    df['Middle'] = df['4. close'].rolling(window=window).mean()
    df['StdDev'] = df['4. close'].rolling(window=window).std()
    df['Upper'] = df['Middle'] + (df['StdDev'] * 2)
    df['Lower'] = df['Middle'] - (df['StdDev'] * 2)
    return df

def run(ticker: str, return_data: bool = False):
    """Wrapper for GUI/CLI use."""
    df = load_or_update(ticker)
    df = bollinger_bands(df)

    last_close = df["Close"].iloc[-1]
    upper = df["Upper"].iloc[-1]
    lower = df["Lower"].iloc[-1]

    if last_close > upper:
        signal = "bearish"
    elif last_close < lower:
        signal = "bullish"
    else:
        signal = "hold"

    if return_data:
        return signal, df
    return signal