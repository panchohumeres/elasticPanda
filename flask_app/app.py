from flask import Flask
from flask import render_template
import os
import socket
import pandas as pd


app = Flask(__name__)


@app.route("/",methods=['GET'])
def show_tables():
    data = pd.read_csv('/data/tweets_Scotland_b_(2).txt',sep='\t')
    #data.set_index(['Name'], inplace=True)
    #data.index.name=None
    #females = data.loc[data.Gender=='f']
    #males = data.loc[data.Gender=='m']
    #return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    #titles = ['na', 'Female surfers', 'Male surfers'])
    return render_template('view.html',tables=[data.to_html(classes='female')],
    titles = ['na', 'Tweets Scotland'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)