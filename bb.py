import pandas as pd
import datetime as dt
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
pd.set_option('mode.chained_assignment', None)
_start = dt.date(2015,1,1)
_end = dt.date(2019,1,1)
ticker = 'RELIANCE.NS'
df = yf.download(ticker, start = _start, end = _end)
df['percent_change']=round((df['Adj Close'].pct_change()),2)
df['MA']=df['Adj Close'].rolling(window=20).mean()
df['std']=df['Adj Close'].rolling(window=20).std()
df['upper_bound']=df['MA']+(2*df['std'])
df['lower_bound']=df['MA']-(2*df['std'])
df=df.dropna(axis=0)
df['signal']=np.where((df['lower_bound']>df['Adj Close']) & (df['Adj Close'].shift(1)>=df['lower_bound']),1,0)
df['signal']=np.where((df['upper_bound']<df['Adj Close']) & (df['Adj Close'].shift(1)<=df['upper_bound']),-1,df['signal'])
df['position'] = df['signal'].replace(to_replace=0, method='ffill')
df['position'] = df['position'].shift(1)
df=df.dropna(axis=0)
df['returns_stat']=df['position']*df['percent_change']
df['thousand_buy']=1000*(1+df['percent_change']).cumprod()
df['returns_stat']=1000*(1+df['returns_stat']).cumprod()
df=df.drop(['Open','High','Low','Volume','Close'],axis=1)