import requests
#import quandl
import pandas
import simplejson as json
from bokeh.plotting import figure, show
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session

app = Flask(__name__)

app.vars={}


@app.route('/')
def main():
      return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
        
@app.route('/result_output_jm', methods=['POST'])
def graph():
    app.vars['ticker'] = request.form['ticker']
    #api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/'+app.vars['ticker']+'.csv?auth_token=okXqsjphs9GQY35trX2B'
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=okXqsjphs9GQY35trX2B' % app.vars['ticker']
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    #quandl.ApiConfig.api_key = 'okXqsjphs9GQY35trX2B'
    #df = quandl.get_table('ZACKS/FC', ticker=app.vars['ticker'])

    a = raw_data.json()
    df = pandas.DataFrame(a['data'], columns=a['column_names'])
    df['Date'] = pandas.to_datetime(df['Date'])
    #print(df['per_end_date'])
    #df = pandas.DataFrame(a['data'], columns=a['column_names'])

    #print(df)
    #df['per_end_date'] = pandas.to_datetime(df['per_end_date'])

    p = figure(title='Stock prices for %s' % app.vars['ticker'], x_axis_label='date',x_axis_type='datetime')
    if request.form.get('Open'):
        p.line(x=df['Date'], y=df['Open'],line_width=2, legend='Open')
        #p.line(x=df['per_end_date'].values, y=df['wavg_shares_out'].values,line_width=2, legend='wavg_shares_out')
        #show(p)
    if request.form.get('High'):
        p.line(x=df['Date'], y=df['High'],line_width=2, line_color="green", legend='High')
        #p.line(x=df['per_end_date'].values, y=df['eps_basic_net'].values,line_width=2, line_color="green", legend='eps_basic_net')
        #show(p)
    if request.form.get('Low'):
        p.line(x=df['Date'], y=df['Low'],line_width=2, line_color="red", legend='Low')
        #p.line(x=df['per_end_date'].values, y=df['eps_diluted_net'].values,line_width=2, line_color="red", legend='eps_diluted_net')
    if request.form.get('Close'):
        p.line(x=df['Date'], y=df['Close'],line_width=2, line_color="orange", legend='Close')
        #show(p)
    script, div = components(p)
    return render_template('result_output_jm.html', script=script, div=div)

if __name__ == '__main__':
    #ps aux | grep "app.py"
    #app.run(port=33507)
    app.run(host='0.0.0.0')
