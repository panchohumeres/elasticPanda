from flask import Flask
from flask import render_template
from flask import request
from redis import Redis, RedisError
from flask import session
import os
import socket
import pandas as pd
#por defecto, las carpetas "static" y "templates" en la misma carpeta de la app (script python)
#flask usa jinja


# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)
app = Flask(__name__)
# Check Configuration section for more details
app.secret_key = 'You Will Never Guess'

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

#https://sarahleejane.github.io/learning/python/2015/08/09/simple-tables-in-webapps-using-flask-and-pandas-with-python.html
#ejemplo con padas
@app.route("/tables")
def show_tables():
    data = pd.read_csv('../../../data/tweets_Scotland_b_(2).txt',sep='\t')
    #data.set_index(['Name'], inplace=True)
    #data.index.name=None
    #females = data.loc[data.Gender=='f']
    #males = data.loc[data.Gender=='m']
    #return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    #titles = ['na', 'Female surfers', 'Male surfers'])
    return render_template('view.html',tables=[data.to_html(classes='female')],
    titles = ['na', 'Tweets Scotland'])

#formularios
#https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
@app.route('/form')
def my_form():
    return render_template('my-form.html')

@app.route('/form', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

@app.route('/multiform')
def multi_form():
    return render_template('hor_form.html')

@app.route('/multiform', methods=['POST'])
def multi_form_post():
    A = request.form['A']
    B=request.form['B']
    C=request.form['C']
    D=request.form['D']

    processed_text = (A+' '+B+' '+C+' '+D).upper()
    return processed_text
#sobre sesiones y permanencia de variables
#https://stackoverflow.com/questions/27611216/how-to-pass-a-variable-between-flask-pages
#https://gist.github.com/macloo/67caf0e0d0718d4723d88786e1db80fb
@app.route('/pandasform')
def pandas_form():
    df={'A':[],'B':[],'C':[],'D':[]}
    session['df']=df #no se pueden guardar dfs en variables de sesion
    return render_template('hor_form.html')


@app.route('/pandasform', methods=['POST'])
def pandas_form_post():
    df=pd.DataFrame.from_dict(session['df'])

    inputs={}
    inputs['A'] = [request.form['A']]
    inputs['B']=[request.form['B']]
    inputs['C']=[request.form['C']]
    inputs['D']=[request.form['D']]


    inputs=pd.DataFrame.from_dict(inputs)
    df=df.append(inputs,ignore_index=True)

    session['df']=df.to_dict(orient='list')

    #deletes=[request.form['del']]
    #deletes=str(deletes)
    # deletes=request.form['del']
    if 'del' in request.form:
        deletes=request.form['del']


    return render_template('pandas_form.html',tables=[df.to_html(classes='female')],
    titles = ['na', 'Your inputs'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)