from flask import Flask, render_template, request, redirect
import numpy as np
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

api_key = 'haHnUHcdK836KppjbVKF'
num_days = 30

csv_url_base = "https://www.quandl.com/api/v3/datasets/WIKI/{stock}.csv?rows={num_rows}?api_key={key}"

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    return 'Oops'

@app.route('/graph', methods=['GET','POST'])
def graph():
  if request.method == 'GET':
    return redirect('/index')
  else:
    ticker = request.form['ticker'].upper()
    plot = figure(x_axis_type = 'datetime', x_axis_label = 'Date', y_axis_label = '%s Stock Price' % ticker)
    try:
      data = pandas.read_csv(filepath_or_buffer=csv_url_base.format(stock=ticker, 
                                                              key=api_key, 
                                                              num_rows=num_days))
      dates = np.array(data['Date'], dtype=np.datetime64)
      for name, color in [('Open', 'red'), ('Close', 'blue')]:
        plot.line(dates, data[name], legend=name, line_width=3, line_color=color)

        script, div = components(plot)

      return render_template('graph.html',
                             script = script,
                             ticker = ticker,
                             graph = div)
    except:
      return render_template('error.html', ticker=ticker)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=33507)
