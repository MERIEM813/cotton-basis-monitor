#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:44:55 2026

@author: meriemifreden
"""

import matplotlib.pyplot as plt
from data_loader import fetch_cotton_futures
from basis_calc import calculate_zscore, detect_regimes
from trading_signal import generate_signals

print("Generating plots...")

# run the whole quant pipeline
df = fetch_cotton_futures()
df = calculate_zscore(df)
df = detect_regimes(df)
df = generate_signals(df)

df['Cumulative_Returns'] = (1 + df['Strategy_Returns']).cumprod() - 1

# plot setup (stacked)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# subplot 1: spot/futures price + signals
ax1.plot(df.index, df['Cotton_Futures_Close'], label='ICE Cotton #2 Price', color='black', alpha=0.6)

longs = df[df['Position'] == 1]
shorts = df[df['Position'] == -1]

ax1.scatter(longs.index, longs['Cotton_Futures_Close'], marker='^', color='green', s=100, label='Long (Z < -2)')
ax1.scatter(shorts.index, shorts['Cotton_Futures_Close'], marker='v', color='red', s=100, label='Short (Z > 2)')
ax1.set_title('Cotton Mean-Reversion: Trading Signals')
ax1.set_ylabel('Price (Cents/lb)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# subplot 2: equity curve
ax2.plot(df.index, df['Cumulative_Returns'] * 100, label='Strategy Returns (%)', color='blue', linewidth=2)
ax2.set_title('Gross Cumulative Performance')
ax2.set_ylabel('Performance (%)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()