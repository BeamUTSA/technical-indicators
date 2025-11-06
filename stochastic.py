import pandas as pd
from core.load_data import load_or_update

def stochastic_oscillator(data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    df = data.copy()

    low_min = df['3. low'].rolling(window=k_period).min()
    high_max = df['2. high'].rolling(window=k_period).max()

    df['%K'] = (df['4. close'] - low_min) * 100 / (high_max - low_min)
    df['%D'] = df['%K'].rolling(window=d_period).mean()

    return df

def run(ticker: str, return_data: bool = False, k: int = 14, d: int = 3):
    """Wrapper for GUI/CLI use."""
    df = load_or_update(ticker)
    df = stochastic_oscillator(df, k, d)

    last_k = df["%K"].iloc[-1]
    last_d = df["%D"].iloc[-1]

    # Signal: Bullish if %K crosses above %D in oversold zone
    if 20 > last_k > last_d:
        signal = "bullish"
    elif 80 < last_k < last_d:
        signal = "bearish"
    else:
        signal = "hold"

    if return_data:
        return signal, df
    return signal
