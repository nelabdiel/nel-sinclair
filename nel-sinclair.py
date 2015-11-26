#In this notebook I'm using the current world records as a base for our formula.
import os
from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.util.string import encode_utf8
import requests
#from bs4 import BeautifulSoup
import math
import numpy as np

app = Flask(__name__)

app.vars = {}

app.vars['color'] = {
    'Male Senior': 'navy',
    #'Female Senior': 'red'
}

#Index page
@app.route('/')
def main():
    return redirect('/index')

#Error page
@app.route('/error-page')
def error_page():
    return render_template('error.html')

#Collecting from index
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['userbw'] = request.form['userbw']
        app.vars['usertotal'] = request.form['usertotal']
        app.vars['features'] = request.form.getlist('features')

        if app.vars['userbw'] == '' or app.vars['usertotal'] == '':
            return redirect('/error-page')

        else:
            
            
            return redirect('/results')
        
@app.route('/results', methods=['GET'])
def graph():
    
    #wr = [(55.62, 305), (61.81, 332), (68.68, 359), (76.40, 380), (84.69, 394), (93.52, 418), (104.76, 436), (147.48,472)]
    
    
    
    
    
    #World Records
    bw = [55.62, 61.81, 68.68, 76.4, 84.69, 93.52, 104.76, 147.48]
    total = [305, 332, 359, 380, 394, 418, 436, 472]
    
    #your performance
    userbw = float(app.vars['userbw'])
    usertotal = float(app.vars['usertotal'])
    
    #your sinclair
    #m = 0.794358141
    #n = 174.393
    
    ts = 0
    #if userbw > n:
        #ts = usertotal
    
    #else:
        #s = math.log(userbw/n, 10)
        #ts = round(usertotal*(10**(m*(s**2))), 2)
    
    #Nel-Sinclair Curve
    a = 85.477722914300003
    b = 41.357074003999998
    c = 0.0060825625000000003
    d = 512.45085465119996
    x = np.linspace(50, 180, 1000)
    approx= a*np.log(c*(x-b))+d
    
    #This years top
    #r = requests.get("http://www.iwf.net/results/ranking-list/?ranking_year=2015&ranking_agegroup=Senior&ranking_gender=M&ranking_category=all&ranking_lifter=all&x=18&y=10")
    #r.content
    #soup = BeautifulSoup(r.content)
    #rows = soup.find_all("tr")
    #webbw = []
    #for row in rows:
        #cells = row.find_all('td')
        #for i, cell in enumerate(cells):
            #if i == 4:
                #webbw.append(cell.text.strip())
            
    #webtotal = []
    #for row in rows:
        #cells = row.find_all('td')
        #for i, cell in enumerate(cells):
            #if i == 7:
                #webtotal.append(cell.text.strip())        
    
    
    p = figure(plot_width=500, plot_height=500)
    p.circle(bw, total, size=10, legend= "World Record")
    p.circle(userbw, usertotal, size=10, color = "green", legend="You")
    #p.circle(webbw, webtotal, size=5, color = "red", legend="Others")
    p.line(x, approx, line_color="#D95B43", line_width=3, alpha=0.7, legend="Nel-Sinclair")
    
    p.title = "Body Weight vs Total"
    p.xaxis.axis_label="Body Weight in Kilos"
    p.yaxis.axis_label="Total in Kilos"
    p.legend.orientation = "top_left"
    
    
    

    p.xgrid.grid_line_color = None
    
    script, div = components(p)
    html = render_template(
        'results.html',
        ts=ts,
        plot_script=script, plot_div=div #, plot_resources=plot_resources
    )
    return encode_utf8(html)        
            
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)          