from flask import Flask
import os
import socket
import pandas as pd
from ssl import create_default_context
from search import Elasticsearch
from flask import Blueprint,render_template,request,jsonify
import json

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



@app.route("/pandas",methods=['GET'])
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



@app.route("/",methods=['GET','POST'],endpoint='index')
def index():
    if request.method=='GET':
        res ={
	            'hits': {'total': 0, 'hits': []}
             }
        return render_template("index.html",res=res)
    elif request.method =='POST':
        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input"]
            print("Search Term:", search_term)
            payload = {
                "query": {
                    "query_string": {
                        "analyze_wildcard": True,
                        "query": str(search_term),
                        "fields": ["",""]
                    }
                },
                "size": 50,
                "sort": [

                ]
            }
            payload = json.dumps(payload)
            #url = "http://search:/hacker/tutorials/_search"
            response = es.search(index=INDEX_NAME,body=body)
            #response_dict_data = json.loads(str(response.text))
            response_dict_data = response
            return render_template('index.html', res=response_dict_data)


@app.route("/autocomplete",methods=['POST'],endpoint='autocomplete')
def autocomplete():
    if request.method == 'POST':
        search_term = request.form["input"]
        print("POST request called")
        print(search_term)
        payload ={
          "autocomplete" : {
            "text" : str(search_term),
            "completion" : {
              "field" : "title_suggest"
            }
          }
        }
        payload = json.dumps(payload)
        url="http://search:/autocomplete/_suggest"
        response = es.search(index=INDEX_NAME,body=body)
        #response_dict_data = json.loads(str(response.text))
        response_dict_data = response
        return json.dumps(response_dict_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)