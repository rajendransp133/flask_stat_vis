from flask import Flask,render_template,send_file,Response
import random
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg  as FigureCanvas
from matplotlib.figure import Figure
import macd as macd
import bb as bb




app = Flask(__name__)



@app.route('/')
def home():
	return render_template('graph.html',start=macd._start,end=macd._end)

@app.route('/BB')
def new_home():
    return render_template('BB.html')

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():

    fig = Figure(figsize=(10,5))
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(macd.df['macd'],color='#ff9900',linewidth=2)
    axis.plot(macd.df['macd_s'],color='#000000',linewidth=2)
    axis.bar(macd.df.index,macd.df['macd_h'].fillna(0), width=0.5, snap=False,color=macd.colors_list)
    return fig

@app.route('/plot_BB.png')
def plot_bb():
    fig = create_bb()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
def create_bb():
    fig=Figure(figsize=(15,5))
    ax1=fig.add_subplot(1,2,1)
    ax2=fig.add_subplot(1,2,2)
    ax1.plot(bb.df[['upper_bound','lower_bound','Adj Close']])
    ax2.plot(bb.df[['thousand_buy','returns_stat']])
    return fig

if __name__ == '__main__':
	app.run()
