import pandas as pd
from core.load_data import load_or_update

"""
RSI indexing for 10 day frames
"""
def relative_strength_index(data: pd.DataFrame, period: int = 10) -> pd.DataFrame:
    df = data.copy()
    delta = df['4. close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def run(ticker: str, return_data: bool = False):
    """Wrapper for GUI/CLI use."""
    df = load_or_update(ticker)
    df = relative_strength_index(df)

    last_rsi = df["RSI"].iloc[-1]
    if last_rsi > 70:
        signal = "bearish"
    elif last_rsi < 30:
        signal = "bullish"
    else:
        signal = "hold"

    if return_data:
        return signal, df
    return signal