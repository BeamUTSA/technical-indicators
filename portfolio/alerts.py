import os
import json
from core.load_data import load_or_update

ALERTS_FILE = os.path.join("data", "alerts.json")

# --- Alerts in memory ---
alerts = []

# --- Persistence helpers ---
def load_alerts():
    global alerts
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            alerts = json.load(f)
        print(f"[INFO] Loaded {len(alerts)} alerts from disk.")
    else:
        alerts = []
        print("[INFO] No alerts file found, starting fresh.")

def save_alerts():
    global alerts
    os.makedirs("data", exist_ok=True)
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)
    print(f"[INFO] Saved {len(alerts)} alerts to disk.")

# --- Core functions ---
def add_alert(portfolio_id, ticker, threshold_price, direction="above"):
    global alerts
    alerts.append({
        "portfolio_id": portfolio_id,
        "ticker": ticker.upper(),
        "threshold": threshold_price,
        "direction": direction
    })
    save_alerts()
    print(f"[INFO] Alert added: {ticker.upper()} {direction} {threshold_price}")

def remove_alert():
    global alerts
    if not alerts:
        print("[INFO] No alerts to remove.")
        return

    print("\n🗑️ Remove Alert")
    for i, alert in enumerate(alerts, 1):
        print(f"{i}. {alert['ticker']} {alert['direction']} {alert['threshold']}")

    try:
        choice = int(input("Enter the number of the alert to remove (0 to cancel): ").strip())
    except ValueError:
        print("[ERROR] Invalid input.")
        return

    if choice == 0:
        print("[INFO] Cancelled.")
        return
    elif 1 <= choice <= len(alerts):
        removed = alerts.pop(choice - 1)
        save_alerts()
        print(f"[INFO] Removed alert: {removed['ticker']} {removed['direction']} {removed['threshold']}")
    else:
        print("[ERROR] Invalid selection.")

def check_alerts():
    global alerts
    if not alerts:
        print("\n🔔 No alerts set.")
        return

    print("\n🔔 Checking alerts...")
    for alert in alerts:
        ticker = alert["ticker"]
        threshold = alert["threshold"]
        direction = alert["direction"]

        try:
            data = load_or_update(ticker)
            latest_price = data["4. close"].iloc[-1]

            triggered = (
                    (direction == "above" and latest_price >= threshold) or
                    (direction == "below" and latest_price <= threshold)
            )

            if triggered:
                print(f"🚨 ALERT: {ticker} is {latest_price:.2f}, {direction} {threshold}")
            else:
                print(f"[OK] {ticker} at {latest_price:.2f}, no trigger ({direction} {threshold})")

        except Exception as e:
            print(f"[ERROR] Could not check {ticker}: {e}")

def view_alerts():
    global alerts
    if not alerts:
        print("[INFO] No alerts set.")
        return

    print("\n📋 Active Alerts:")
    for i, alert in enumerate(alerts, 1):
        ticker = alert["ticker"]
        threshold = alert["threshold"]
        direction = alert["direction"]

        try:
            data = load_or_update(ticker)
            latest_price = data["4. close"].iloc[-1]
            print(f"{i}. {ticker} {direction} {threshold} | Current: {latest_price:.2f}")
        except Exception as e:
            print(f"{i}. {ticker} {direction} {threshold} | [ERROR] Could not fetch price: {e}")
