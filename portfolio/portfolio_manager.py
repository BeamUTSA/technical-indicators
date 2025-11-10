import pandas as pd
from core.load_data import load_or_update

# --- Dummy Portfolio Data ---
portfolio = [
    {"ticker": "AAPL", "shares": 10},
    {"ticker": "NVDA", "shares": 5},
    {"ticker": "TSLA", "shares": 3},
]

# --- Cash Balance ---
cash_balance = 10000.00  # starting cash

def view_portfolio():
    """View a dummy portfolio table with total value, allocation %, and cash balance."""
    rows = []
    total_value = 0.0

    for holding in portfolio:
        symbol = holding["ticker"]
        shares = holding["shares"]

        # Get latest price
        data = load_or_update(symbol)
        latest_price = data["4. close"].iloc[-1]

        value = latest_price * shares
        total_value += value

        rows.append({
            "Ticker": symbol,
            "Price": round(latest_price, 2),
            "Shares": shares,
            "Total Value": round(value, 2)
        })

    # Add allocation %
    for row in rows:
        row["Allocation %"] = round((row["Total Value"] / total_value) * 100, 2) if total_value > 0 else 0

    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["Ticker", "Price", "Shares", "Total Value", "Allocation %"])

    print("\n📊 Portfolio Overview")
    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("[INFO] Portfolio is empty.")

    print(f"\n💰 Portfolio Holdings Value: ${round(total_value, 2)}")
    print(f"💵 Available Cash: ${round(cash_balance, 2)}")
    print(f"📈 Total Portfolio Value: ${round(total_value + cash_balance, 2)}")


def edit_portfolio():
    """Edit the dummy portfolio by buying or selling shares with cash constraints."""
    global cash_balance, portfolio

    print("\n📝 Edit Portfolio")
    print("1. Buy Stock")
    print("2. Sell Stock")
    print("0. Cancel")

    choice = input("Choose an option: ").strip()

    if choice == "0":
        return

    ticker = input("Enter ticker symbol: ").upper().strip()
    try:
        shares = int(input("Enter number of shares: ").strip())
    except ValueError:
        print("[ERROR] Please enter a valid number of shares.")
        return

    # Fetch latest price for cost calculation
    try:
        data = load_or_update(ticker)
        latest_price = data["4. close"].iloc[-1]
    except Exception as e:
        print(f"[ERROR] Could not fetch price for {ticker}: {e}")
        return

    if choice == "1":  # Buy
        cost = latest_price * shares
        if cash_balance >= cost:
            for holding in portfolio:
                if holding["ticker"] == ticker:
                    holding["shares"] += shares
                    cash_balance -= cost
                    print(f"[INFO] Bought {shares} shares of {ticker} at ${latest_price:.2f}. Remaining cash: ${cash_balance:.2f}")
                    return
            # If ticker not in portfolio, add it
            portfolio.append({"ticker": ticker, "shares": shares})
            cash_balance -= cost
            print(f"[INFO] Added new holding: {ticker}, {shares} shares at ${latest_price:.2f}. Remaining cash: ${cash_balance:.2f}")
        else:
            print(f"[ERROR] Not enough cash. Needed ${cost:.2f}, available ${cash_balance:.2f}.")

    elif choice == "2":  # Sell
        for holding in portfolio:
            if holding["ticker"] == ticker:
                if holding["shares"] > shares:
                    holding["shares"] -= shares
                    revenue = latest_price * shares
                    cash_balance += revenue
                    print(f"[INFO] Sold {shares} shares of {ticker} at ${latest_price:.2f}. New cash: ${cash_balance:.2f}")
                elif holding["shares"] == shares:
                    portfolio.remove(holding)
                    revenue = latest_price * shares
                    cash_balance += revenue
                    print(f"[INFO] Sold all shares of {ticker}, removed from portfolio. New cash: ${cash_balance:.2f}")
                else:
                    print(f"[ERROR] Not enough shares to sell. You own {holding['shares']}.")
                return
        print(f"[ERROR] {ticker} not found in portfolio.")

    else:
        print("Invalid choice.")
