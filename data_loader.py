#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:24:53 2026

@author: meriemifreden
"""
import yfinance as yf
import pandas as pd

def fetch_cotton_futures(start_date="2018-01-01", end_date=None):
    # pulling historical data for ICE Cotton #2 (ticker: CT=F)
    print("Downloading ICE Cotton #2 data...")
    
    cotton_data = yf.download("CT=F", start=start_date, end=end_date)
    
    # just keeping the close price for now
    df = pd.DataFrame(cotton_data['Close'])
    df.columns = ['Cotton_Futures_Close']
    
    df = df.dropna() # drop nans to avoid messing up the pipeline
    
    print(f"Got {len(df)} trading days.")
    return df

if __name__ == "__main__":
    df_futures = fetch_cotton_futures()
    print(df_futures.tail())