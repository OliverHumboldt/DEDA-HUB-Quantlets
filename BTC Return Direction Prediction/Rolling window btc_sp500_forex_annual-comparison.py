import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. Define Tickers and Exact Slide Dates ---
tickers_map = {
    'BTC-USD': 'Bitcoin',
    '^GSPC': 'S&P 500',
    'EURUSD=X': 'EUR/USD'
}

# Dates matching the x-axis of your original slide
start_date = "2025-07-01"
end_date = "2026-05-31"

print(f"Downloading real market data from {start_date} to {end_date}...")
raw_data = yf.download(list(tickers_map.keys()),
                       start=start_date, end=end_date, progress=False)

# --- 2. Safely Extract and Clean Data ---
if 'Adj Close' in raw_data.columns:
    data = raw_data['Adj Close']
elif 'Close' in raw_data.columns:
    data = raw_data['Close']
else:
    raise ValueError("Could not find closing price data.")

# Rename columns to match the slide legend and fill missing weekend data
data = data.rename(columns=tickers_map)
data = data.ffill()

# --- 3. Calculate Volatility ---
daily_returns = data.pct_change()
volatility = daily_returns.rolling(window=30).std() * np.sqrt(252) * 100
volatility = volatility.dropna()

# --- 4. Create the Chart ---
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(volatility.index, volatility['Bitcoin'],
        label='Bitcoin', color='#1f77b4', linewidth=1.5)
ax.plot(volatility.index, volatility['S&P 500'],
        label='S&P 500', color='#ff7f0e', linewidth=1.5)
ax.plot(volatility.index, volatility['EUR/USD'],
        label='EUR/USD', color='#2ca02c', linewidth=1.5)

ax.set_title(
    'Rolling 30-Day Annualized Volatility Comparison\nBitcoin vs S&P 500 vs EUR/USD', fontsize=12)
ax.set_xlabel('Date', fontsize=10)
ax.set_ylabel('Annualized Volatility (%)', fontsize=10)

ax.grid(True, linestyle='-', alpha=0.5)
ax.legend(loc='upper right', fontsize=9)

# --- 5. Force Transparency ---
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# --- 6. Save to an EXACT Location ---
save_folder = r"C:\Users\lenovo\OneDrive\Desktop\Courses\digital_economy\project on bitcoin\FULL PROJECT\LR"
filename = "volatility_slide_dates_transparent.png"

os.makedirs(save_folder, exist_ok=True)
full_path = os.path.join(save_folder, filename)

plt.savefig(full_path, dpi=300, bbox_inches='tight', transparent=True)

print("\n" + "="*70)
print(f"SUCCESS! The transparent chart for Jul 2025 - May 2026 is saved at:")
print(full_path)
print("="*70 + "\n")

plt.close()
