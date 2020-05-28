from flask import Flask
from flask import render_template
import os
import socket
import pandas as pd
from ssl import create_default_context
from search import Elasticsearch

app = Flask(__name__)

ES_HOST = "examplePass"
INDEX_NAME = ''

context = create_default_context(cafile="/certs/ca/ca.crt")
es = Elasticsearch(
    [ES_HOST],
    http_auth=('', ''),
    scheme="https",
    port=443,
    ssl_context=context,
)

body={
  "query": {
    "multi_match" : {
      "query":      "",
      "type":       "most_fields",
      "fields":     [ "", ""]
    }
  }
}



@app.route("/",methods=['GET'])
def search():
    res= es.search(index=INDEX_NAME,body=body)
    hits=[]

    for h in res['hits']['hits']:
        hits.append(h['_source'])
    hits=pd.DataFrame(hits)
    #data = pd.read_csv('/data/tweets_Scotland_b_(2).txt',sep='\t')
    #data.set_index(['Name'], inplace=True)
    #data.index.name=None
    #females = data.loc[data.Gender=='f']
    #males = data.loc[data.Gender=='m']
    #return render_template('view.html',tables=[females.to_html(classes='female'), males.to_html(classes='male')],
    #titles = ['na', 'Female surfers', 'Male surfers'])
    return render_template('view.html',tables=[hits.to_html(classes='female')],
    titles = ['na', ''])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)