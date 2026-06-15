#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:41:41 2026

@author: meriemifreden
"""

import pandas as pd
import numpy as np

def generate_signals(df):
    # basic mean-reversion algo
    # short when overbought (Z > 2), long when oversold (Z < -2)
    signals = []
    current_position = 0  # 0 = flat, 1 = long, -1 = short
    
    for idx, row in df.iterrows():
        z = row['Z_Score']
        
        if current_position == 0:
            if z > 2.0:
                current_position = -1  # short the anomaly
            elif z < -2.0:
                current_position = 1   # buy the dip
        elif current_position == 1 and z >= 0:
            current_position = 0       # exit long
        elif current_position == -1 and z <= 0:
            current_position = 0       # exit short
            
        signals.append(current_position)
        
    df['Position'] = signals
    
    df['Market_Returns'] = df['Cotton_Futures_Close'].pct_change()
    # shift(1) is super important here to avoid look-ahead bias!!
    df['Strategy_Returns'] = df['Position'].shift(1) * df['Market_Returns']
    
    return df

if __name__ == "__main__":
    from data_loader import fetch_cotton_futures
    from basis_calc import calculate_zscore, detect_regimes
    
    df = fetch_cotton_futures()
    df = calculate_zscore(df)
    df = detect_regimes(df)
    df_signals = generate_signals(df)
    
    cum_returns = (1 + df_signals['Strategy_Returns'].dropna()).cumprod() - 1
    print(f"Sim done. Gross cum returns: {cum_returns.iloc[-1]*100:.2f}%")