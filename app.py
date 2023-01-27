from flask import Flask,render_template,send_file,Response
import random
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg  as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import datetime as dt
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


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

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('graph.html',start=_start,end=_end)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():

    fig = Figure(figsize=(10,5))
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(df['macd'],color='#ff9900',linewidth=2)
    axis.plot(df['macd_s'],color='#000000',linewidth=2)
    axis.bar(df.index,df['macd_h'].fillna(0), width=0.5, snap=False,color=colors_list)
    return fig

if __name__ == '__main__':
	app.run()
