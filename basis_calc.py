#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:32:32 2026

@author: meriemifreden
"""

import pandas as pd
import numpy as np

def calculate_zscore(df, column_name='Cotton_Futures_Close', window=20):
    # rolling z-score to catch price anomalies 
    # 20 days window seems standard for short term dynamics
    rolling_mean = df[column_name].rolling(window=window).mean()
    rolling_std = df[column_name].rolling(window=window).std()
    
    df['Z_Score'] = (df[column_name] - rolling_mean) / rolling_std
    return df

def detect_regimes(df, threshold=2.0):
    # isolate tail events (top 5% extreme moves)
    df['Regime'] = 0
    df.loc[df['Z_Score'] > threshold, 'Regime'] = 1
    df.loc[df['Z_Score'] < -threshold, 'Regime'] = -1
    
    return df.dropna()

if __name__ == "__main__":
    from data_loader import fetch_cotton_futures
    
    df = fetch_cotton_futures()
    df_stats = calculate_zscore(df)
    df_regimes = detect_regimes(df_stats)
    
    extremes = df_regimes[df_regimes['Regime'] != 0]
    print(f"Found {len(extremes)} days in extreme regime")