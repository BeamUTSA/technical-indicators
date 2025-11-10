from portfolio.portfolio_manager import view_portfolio, edit_portfolio
from portfolio.alerts import add_alert, remove_alert, view_alerts, check_alerts, load_alerts
from strategies.moving_avg import moving_average_crossover
from strategies.rsi import relative_strength_index
from strategies.bollinger import bollinger_bands
from analysis.outlook import get_outlook
from core.load_data import load_or_update

def strategies_menu():
    while True:
        print("\n📊 Strategies Menu")
        print("1. Moving Average Crossover")
        print("2. RSI")
        print("3. Bollinger Bands")
        print("4. Run All Strategies")
        print("0. Back to Main Menu")

        choice = input("Choose a strategy: ").strip()

        if choice == "0":
            break

        if choice in ["1", "2", "3", "4"]:
            symbol = input("Enter ticker symbol (e.g., AAPL): ").upper().strip()
            try:
                data = load_or_update(symbol)

                if choice == "1":
                    result = moving_average_crossover(data)
                    outlook = get_outlook("moving_avg", result)
                    print("\n📊 Last 5 rows of data:")
                    print(result.tail(5))
                    print(f"\n[OUTLOOK] {symbol}: {outlook}")

                elif choice == "2":
                    result = relative_strength_index(data)
                    outlook = get_outlook("rsi", result)
                    print("\n📊 Last 5 rows of data:")
                    print(result.tail(5))
                    print(f"\n[OUTLOOK] {symbol}: {outlook}")

                elif choice == "3":
                    result = bollinger_bands(data)
                    outlook = get_outlook("bollinger", result)
                    print("\n📊 Last 5 rows of data:")
                    print(result.tail(5))
                    print(f"\n[OUTLOOK] {symbol}: {outlook}")

                elif choice == "4":
                    print(f"\n📊 Running all strategies for {symbol}...")

                    ma_result = moving_average_crossover(data)
                    ma_outlook = get_outlook("moving_avg", ma_result)

                    rsi_result = relative_strength_index(data)
                    rsi_outlook = get_outlook("rsi", rsi_result)

                    bb_result = bollinger_bands(data)
                    bb_outlook = get_outlook("bollinger", bb_result)

                    print("\n📋 Consolidated Report")
                    print(f"Moving Average Crossover: {ma_outlook}")
                    print(f"RSI: {rsi_outlook}")
                    print(f"Bollinger Bands: {bb_outlook}")

            except Exception as e:
                print(f"[ERROR] {e}")
        else:
            print("Invalid choice.")

def alerts_menu():
    while True:
        print("\n🔔 Alerts Menu")
        print("1. View Alerts")
        print("2. Add Alert")
        print("3. Remove Alert")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            view_alerts()
        elif choice == "2":
            ticker = input("Enter ticker symbol: ").upper().strip()
            threshold = float(input("Enter threshold price: ").strip())
            direction = input("Direction (above/below): ").lower().strip()
            add_alert(1, ticker, threshold, direction)
        elif choice == "3":
            remove_alert()
        else:
            print("Invalid choice. Try again.")

def main_menu():
    load_alerts()  # load persisted alerts at startup

    while True:
        check_alerts()  # always check alerts before showing menu

        print("\n📈 Stock Portfolio Tracker (Menu)")
        print("1. View Portfolio")
        print("2. Edit Portfolio (buy/sell)")
        print("3. Strategies")
        print("4. Alerts")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                view_portfolio()
            elif choice == "2":
                edit_portfolio()
            elif choice == "3":
                strategies_menu()
            elif choice == "4":
                alerts_menu()
            elif choice == "0":
                print("Exiting... Goodbye 👋")
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main_menu()
