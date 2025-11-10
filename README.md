# Technical Indicators – Stock Tracker API

This repository contains reusable technical indicator scripts for use within the Stock Tracker API system. Each indicator module exposes a consistent run() function for use in CLI tools, GUI components, and backtesting environments. Data for each indicator is retrieved using the shared loader function:

from core.load_data import load_or_update

-------------------------------------------------------------------------------

## 1. Relative Strength Index (RSI) — rsi.py
Type: Momentum Oscillator  
Purpose: Detects overbought and oversold conditions by comparing average gains and losses.

Parameters:
- period: int, default 10 (rolling window size)

Signal Logic:
- RSI > 70 -> bearish
- RSI < 30 -> bullish
- otherwise -> hold

Example:
```python
from strategies import rsi
signal, df = rsi.run("AAPL", period=14, return_data=True)
```

-------------------------------------------------------------------------------

## 2. Moving Average Crossover — moving_avg.py
Type: Trend-following  
Purpose: Detects trend direction by comparing short and long simple moving averages.

Parameters:
- short: int, default 20 (short SMA window)
- long: int, default 50 (long SMA window)

Signal Logic:
- short MA > long MA -> bullish
- short MA < long MA -> bearish
- equal -> hold

Example:
```python
from strategies import moving_avg
signal, df = moving_avg.run("MSFT", short=50, long=200, return_data=True)
```

-------------------------------------------------------------------------------

## 3. Bollinger Bands — bollinger.py
Type: Volatility Indicator  
Purpose: Measures volatility using a moving average and standard deviation bands.

Parameters:
- window: int, default 20 (rolling mean window)
- num_std: int, default 2 (std deviation multiplier)

Signal Logic:
- close > upper band -> bearish
- close < lower band -> bullish
- otherwise -> hold

Example:
```python
from strategies import bollinger
signal, df = bollinger.run("TSLA", window=30, num_std=3, return_data=True)
```

-------------------------------------------------------------------------------

## 4. MACD (Moving Average Convergence Divergence) — macd.py
Type: Momentum and Trend  
Purpose: Measures momentum by comparing two EMAs and a signal line.

Parameters:
- short: int, default 12 (fast EMA)
- long: int, default 26 (slow EMA)
- signal: int, default 9 (signal EMA)

Signal Logic:
- MACD > signal line -> bullish
- MACD < signal line -> bearish
- equal -> hold

Example:
```python
from strategies import macd
signal, df = macd.run("NVDA", short=12, long=26, signal=9, return_data=True)
```

-------------------------------------------------------------------------------

## 5. Average True Range (ATR) — atr.py
Type: Volatility  
Purpose: Measures average volatility using true range.

Parameters:
- period: int, default 14 (ATR rolling window)

Signal Logic:
- ATR above moving average -> high volatility
- ATR below moving average -> low volatility

Example:
```python
from strategies import atr
volatility, df = atr.run("AMZN", period=14, return_data=True)
```

-------------------------------------------------------------------------------

## 6. Stochastic Oscillator — stochastic.py
Type: Momentum  
Purpose: Compares closing price to the recent high-low range.

Parameters:
- k: int, default 14 (K period)
- d: int, default 3 (D smoothing period)

Signal Logic:
- %K < 20 and rising above %D -> bullish
- %K > 80 and falling below %D -> bearish
- otherwise -> hold

Example:
```python
from strategies import stochastic
signal, df = stochastic.run("GOOG", k=14, d=3, return_data=True)
```

-------------------------------------------------------------------------------

## Integration Notes

All indicators assume the price data contains the following fields:
"2. high", "3. low", "4. close", "5. volume"

Each run() function returns:
- a signal ("bullish", "bearish", "hold", or volatility state)
- optionally, a DataFrame if return_data=True

-------------------------------------------------------------------------------

## Example Combined Usage

``` python
from strategies import rsi, macd, bollinger

tickers = ["AAPL", "MSFT", "TSLA"]
for t in tickers:
    print(
        t,
        rsi.run(t),
        macd.run(t),
        bollinger.run(t)
    )
```

-------------------------------------------------------------------------------

## Folder Structure

``` file
strategies/
    atr.py
    bollinger.py
    macd.py
    moving_avg.py
    rsi.py
    stochastic.py
```

-------------------------------------------------------------------------------

## Requirements

Python 3.10 or higher  
pandas 2.0 or higher  
numpy 1.24 or higher  

Install dependencies:
pip install pandas numpy

-------------------------------------------------------------------------------

## License

See LICENSE for usage and distribution terms.

Author: BeamUTSA  
Repository: https://github.com/BeamUTSA/technical-indicators
