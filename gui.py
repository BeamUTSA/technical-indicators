import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QTabWidget, QLabel, QPushButton, QHBoxLayout,
    QLineEdit, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt

from portfolio.portfolio_manager import portfolio, cash_balance
from core.load_data import load_or_update
from portfolio import alerts
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt



# --------------------
# Portfolio Tab
# --------------------
class PortfolioTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Ticker", "Shares", "Price", "Total Value", "Triggered Alerts"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.cash_label = QLabel()
        self.total_label = QLabel()
        layout.addWidget(self.cash_label)
        layout.addWidget(self.total_label)

        # Pie chart area
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.load_portfolio()

    def load_portfolio(self):
        rows = []
        total_value = 0.0
        alerts.load_alerts()
        investments = {}

        for holding in portfolio:
            ticker = holding["ticker"]
            shares = holding["shares"]

            triggered = []
            try:
                data = load_or_update(ticker)
                latest_price = data["4. close"].iloc[-1]
                value = latest_price * shares
                total_value += value
                investments[ticker] = value

                # Check alerts
                for alert in alerts.alerts:
                    if alert["ticker"].upper() == ticker.upper():
                        if alert["direction"] == "above" and latest_price > alert["threshold"]:
                            triggered.append(f"Above {alert['threshold']}")
                        elif alert["direction"] == "below" and latest_price < alert["threshold"]:
                            triggered.append(f"Below {alert['threshold']}")

                trigger_text = ", ".join(triggered) if triggered else "—"
                rows.append((ticker, shares, round(latest_price, 2), round(value, 2), trigger_text))
            except Exception as e:
                rows.append((ticker, shares, "ERR", "ERR", "ERR"))
                print(f"[ERROR] Could not fetch {ticker}: {e}")

        # Update table
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if j == 4 and val != "—" and val != "ERR":
                    item.setForeground(Qt.GlobalColor.red)
                self.table.setItem(i, j, item)

        # Update summary
        self.cash_label.setText(f"💵 Available Cash: ${cash_balance:,.2f}")
        self.total_label.setText(f"💰 Total Portfolio Value: ${cash_balance + total_value:,.2f}")

        # Draw pie chart
        self.ax.clear()
        labels = list(investments.keys()) + ["Cash"]
        values = list(investments.values()) + [cash_balance]
        self.ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        self.ax.set_title("Portfolio Allocation")
        self.canvas.draw()

# --------------------
# Alerts Tab
# --------------------
class AlertsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Ticker", "Direction", "Threshold"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        form_layout = QHBoxLayout()
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Ticker (e.g., AAPL)")
        form_layout.addWidget(self.ticker_input)

        self.direction_input = QComboBox()
        self.direction_input.addItems(["above", "below"])
        form_layout.addWidget(self.direction_input)

        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("Threshold Price")
        form_layout.addWidget(self.threshold_input)

        self.add_button = QPushButton("Add Alert")
        self.add_button.clicked.connect(self.add_alert)
        form_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_alert)
        form_layout.addWidget(self.remove_button)

        layout.addLayout(form_layout)
        self.setLayout(layout)

        self.load_alerts()

    def load_alerts(self):
        alerts.load_alerts()
        self.table.setRowCount(len(alerts.alerts))
        for i, alert in enumerate(alerts.alerts):
            self.table.setItem(i, 0, QTableWidgetItem(alert["ticker"]))
            self.table.setItem(i, 1, QTableWidgetItem(alert["direction"]))
            self.table.setItem(i, 2, QTableWidgetItem(str(alert["threshold"])))

    def add_alert(self):
        ticker = self.ticker_input.text().upper().strip()
        direction = self.direction_input.currentText()
        try:
            threshold = float(self.threshold_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Threshold must be a number.")
            return

        alerts.add_alert(1, ticker, threshold, direction)
        self.load_alerts()

        self.ticker_input.clear()
        self.threshold_input.clear()

    def remove_alert(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select an alert to remove.")
            return

        removed = alerts.alerts.pop(selected)
        alerts.save_alerts()
        self.load_alerts()
        QMessageBox.information(
            self,
            "Alert Removed",
            f"Removed {removed['ticker']} {removed['direction']} {removed['threshold']}",
        )


# --------------------
# Strategies Tab
# --------------------
class StrategiesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # --- Ticker input ---
        ticker_layout = QHBoxLayout()
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Enter ticker (e.g., AAPL)")
        ticker_layout.addWidget(QLabel("Ticker:"))
        ticker_layout.addWidget(self.ticker_input)
        layout.addLayout(ticker_layout)

        # --- Strategy selector ---
        self.strategy_input = QComboBox()
        self.strategy_input.addItems([
            "Moving Average Crossover",
            "RSI",
            "Bollinger Bands",
            "Run All Strategies"
        ])
        layout.addWidget(self.strategy_input)

        # --- Run button ---
        self.run_button = QPushButton("Run Strategy")
        self.run_button.clicked.connect(self.run_strategy)
        layout.addWidget(self.run_button)

        # --- Results label ---
        self.result_label = QLabel("Results will appear here.")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_strategy(self):
        """Run the selected strategy on the given ticker."""
        from strategies import moving_avg, rsi, bollinger
        from analysis import outlook

        ticker = self.ticker_input.text().upper().strip()
        if not ticker:
            QMessageBox.warning(self, "Input Error", "Please enter a ticker symbol.")
            return

        selected = self.strategy_input.currentText()
        results = {}

        try:
            if selected == "Moving Average Crossover":
                signal, df = moving_avg.run(ticker, return_data=True)
                results["Moving Average"] = outlook.interpret("moving_avg", df)
                self.show_moving_avg_chart(df, ticker)

            elif selected == "RSI":
                signal, df = rsi.run(ticker, return_data=True)
                results["RSI"] = outlook.interpret("rsi", df)
                self.plot_rsi(df, ticker)

            elif selected == "Bollinger Bands":
                signal, df = bollinger.run(ticker, return_data=True)
                results["Bollinger"] = outlook.interpret("bollinger", df)
                self.plot_bollinger(df, ticker)

            elif selected == "Run All Strategies":
                ma_signal, ma_df = moving_avg.run(ticker, return_data=True)
                rsi_signal, rsi_df = rsi.run(ticker, return_data=True)
                bb_signal, bb_df = bollinger.run(ticker, return_data=True)

                results["Moving Average"] = outlook.interpret("moving_avg", ma_df)
                results["RSI"] = outlook.interpret("rsi", rsi_df)
                results["Bollinger"] = outlook.interpret("bollinger", bb_df)

                # Show MA chart by default for "Run All"
                self.show_moving_avg_chart(ma_df, ticker)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to run strategy: {e}")
            return

        # Build text summary
        text = f"📊 Strategy results for {ticker}:\n"
        for name, result in results.items():
            text += f"- {name}: {result}\n"

        self.result_label.setText(text)

    # ---------------------
    # Plotting helpers
    # ---------------------
    def plot_moving_avg(self, df, ticker):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(df.index, df["Close"], label="Price")
        plt.plot(df.index, df["SMA_short"], label="Short MA")
        plt.plot(df.index, df["SMA_long"], label="Long MA")
        plt.title(f"{ticker} - Moving Average Crossover")
        plt.legend()
        plt.show()

    def plot_rsi(self, df, ticker):
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(df.index, df["Close"], label="Price")
        ax1.set_title(f"{ticker} - RSI Strategy")
        ax1.legend()
        ax2.plot(df.index, df["RSI"], label="RSI", color="purple")
        ax2.axhline(70, linestyle="--", color="red")
        ax2.axhline(30, linestyle="--", color="green")
        ax2.legend()
        plt.show()

    def plot_bollinger(self, df, ticker):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(df.index, df["Close"], label="Price")
        plt.plot(df.index, df["Upper"], label="Upper Band", linestyle="--")
        plt.plot(df.index, df["Lower"], label="Lower Band", linestyle="--")
        plt.fill_between(df.index, df["Lower"], df["Upper"], alpha=0.2)
        plt.title(f"{ticker} - Bollinger Bands")
        plt.legend()
        plt.show()

    # ---------------------
    # Plotting helpers
    # ---------------------
    def show_moving_avg_chart(self, df, ticker):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(df.index, df["Close"], label="Price")
        plt.plot(df.index, df["MA_Short"], label="Short MA")
        plt.plot(df.index, df["MA_Long"], label="Long MA")
        plt.title(f"{ticker} - Moving Average Crossover")
        plt.legend()
        plt.show()

    def show_rsi_chart(self, df, ticker):
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(df.index, df["Close"], label="Price")
        ax1.set_title(f"{ticker} - RSI Strategy")
        ax1.legend()
        ax2.plot(df.index, df["RSI"], label="RSI", color="purple")
        ax2.axhline(70, linestyle="--", color="red")
        ax2.axhline(30, linestyle="--", color="green")
        ax2.legend()
        plt.show()

    def show_bollinger_chart(self, df, ticker):
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(df.index, df["Close"], label="Price")
        plt.plot(df.index, df["Upper"], label="Upper Band", linestyle="--")
        plt.plot(df.index, df["Lower"], label="Lower Band", linestyle="--")
        plt.fill_between(df.index, df["Lower"], df["Upper"], alpha=0.2)
        plt.title(f"{ticker} - Bollinger Bands")
        plt.legend()
        plt.show()


# --------------------
# Main Window
# --------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Stock Portfolio Tracker")
        self.resize(950, 600)

        self.tabs = QTabWidget()
        self.portfolio_tab = PortfolioTab()
        self.alerts_tab = AlertsTab()
        self.strategies_tab = StrategiesTab()

        self.tabs.addTab(self.portfolio_tab, "Portfolio")
        self.tabs.addTab(self.alerts_tab, "Alerts")
        self.tabs.addTab(self.strategies_tab, "Strategies")

        self.tabs.currentChanged.connect(self.on_tab_change)
        self.setCentralWidget(self.tabs)

    def on_tab_change(self, index):
        if self.tabs.tabText(index) == "Portfolio":
            self.portfolio_tab.load_portfolio()
        elif self.tabs.tabText(index) == "Alerts":
            self.alerts_tab.load_alerts()


# --------------------
# Entry Point
# --------------------
def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
