def get_outlook(strategy_name: str, df):
    latest = df.iloc[-1]  # most recent row

    if strategy_name == "moving_avg":
        if latest['Signal'] == 1:
            return "Bullish"
        elif latest['Signal'] == -1:
            return "Bearish"
        else:
            return "Hold"

    elif strategy_name == "rsi":
        if latest['RSI'] > 70:
            return "Bearish (Overbought)"
        elif latest['RSI'] < 30:
            return "Bullish (Oversold)"
        else:
            return "Hold"

    elif strategy_name == "bollinger":
        price = latest['4. close']
        if price > latest['Upper']:
            return "Bearish (Above Upper Band)"
        elif price < latest['Lower']:
            return "Bullish (Below Lower Band)"
        else:
            return "Hold"

    else:
        return "Unknown Strategy"

def interpret(strategy_name: str, signal_or_df):
    """
    Convenience wrapper:
    - If a DataFrame is passed, fall back to get_outlook().
    - If a raw signal string ('bullish', etc.) is passed, format it nicely.
    """
    if hasattr(signal_or_df, "iloc"):  # DataFrame
        return get_outlook(strategy_name, signal_or_df)

    # Otherwise assume it's a raw signal string
    mapping = {
        "bullish": "📈 Bullish",
        "bearish": "📉 Bearish",
        "hold": "⏸ Hold"
    }
    return mapping.get(str(signal_or_df).lower(), "❓ Unknown")