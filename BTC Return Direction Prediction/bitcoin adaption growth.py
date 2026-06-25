import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

# --- 1. Fetch 10 Years of Real Market Data ---
ticker_symbol = 'BTC-USD'
print(
    f"Downloading the last 10 years of market volume data for {ticker_symbol}...")

# Using period='10y' automatically grabs exactly 10 years from today's date
raw_data = yf.download(ticker_symbol, period='10y', progress=False)

# --- 2. Extract and Smooth Volume Data ---
if 'Volume' in raw_data.columns:
    volume_data = raw_data['Volume']
else:
    raise ValueError("Could not find Volume data.")

# Smooth the data with a 30-day rolling average to show the macro trend
smoothed_volume = volume_data.rolling(window=30).mean().dropna()

# --- 3. Create the Chart ---
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(smoothed_volume.index, smoothed_volume.values,
        color='#1f77b4', linewidth=2.0)

ax.set_title(
    'Bitcoin Network Activity & Adoption Proxy (10-Year Trend)\n(30-Day Rolling Transaction Volume)', fontsize=12)
ax.set_xlabel('Date', fontsize=10)
ax.set_ylabel('Trading Volume (USD)', fontsize=10)

# Format the y-axis to show billions (B) for a cleaner look on the slide


def billions_formatter(x, pos):
    if x >= 1e9:
        return f'${x / 1e9:.0f}B'
    elif x >= 1e6:
        return f'${x / 1e6:.0f}M'
    else:
        return f'${x:.0f}'


ax.yaxis.set_major_formatter(ticker.FuncFormatter(billions_formatter))

ax.grid(True, linestyle='-', alpha=0.5)

# --- 4. Force Transparency ---
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# --- 5. Save to Your Exact Location ---
save_folder = r"C:\Users\lenovo\OneDrive\Desktop\Courses\digital_economy\project on bitcoin\FULL PROJECT\LR"
filename = "bitcoin_10yr_adoption_transparent.png"

os.makedirs(save_folder, exist_ok=True)
full_path = os.path.join(save_folder, filename)

plt.savefig(full_path, dpi=300, bbox_inches='tight', transparent=True)

print("\n" + "="*70)
print(f"SUCCESS! Your 10-year transparent chart is saved at:")
print(full_path)
print("="*70 + "\n")

plt.close()
