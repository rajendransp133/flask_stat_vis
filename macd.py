import pandas as pd
import datetime as dt
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
pd.set_option('mode.chained_assignment', None)

_start = dt.date(2022,1,27)
_end = dt.date(2023,1,27)
ticker = '^NSEI'
df = yf.download(ticker, start = _start, end = _end)
df['percent_change']=round((df['Adj Close'].pct_change()),2)
k = df['Adj Close'].ewm(span=12, adjust=False, min_periods=12).mean()
d = df['Adj Close'].ewm(span=26, adjust=False, min_periods=12).mean()
macd = k - d
df['macd']=k-d
df['macd_s'] = macd.ewm(span=9, adjust=False, min_periods=9).mean() 
df['macd_h']=df['macd'] - df['macd_s']
df=df.drop(['Open','High','Low','Volume','Close'],axis=1)
df=df.dropna(axis=0)
colors_list = np.where(df['macd_h'] < 0, '#000', '#ff9900')