from flask import Flask
import os
import socket
import pandas as pd
from ssl import create_default_context
from elasticsearch import Elasticsearch
from flask import Blueprint,render_template,request,jsonify
import json
import sys

app = Flask(__name__)



#context = create_default_context(cafile="/certs/ca/ca.crt")
sys.path.append('..')
from args.templateVars import *

args={}
args['elastic_user']=os.environ['ELASTIC_USER']
args['elastic_psswd']=os.environ['ELASTIC_PASSWD']
args['DOMAIN_ELASTIC']=os.environ['DOMAIN_ELASTIC']
args['ELASTIC_PORT']=os.environ['ELASTIC_PORT']
args['MODE']=os.environ['MODE']

ES_HOST = 'https://'+args['DOMAIN_ELASTIC']


if args['MODE']=="internal":
  es = Elasticsearch(
      [ES_HOST],
      http_auth=(''),
      scheme="https",
      port=443,
      ssl_context=context,
  )
else:
  es= Elasticsearch(ES_HOST, http_auth=(args['elastic_user'], args['elastic_psswd']),use_ssl=True, verify_certs=False)

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
    titles = ['na', 'Chile Atiende Browser'])

@app.route("/",methods=['GET','POST'],endpoint='index')
def index():
    if request.method=='GET':
        res ={
	            'hits': {'total': 0, 'hits': []}
             }
        INDEX_NAME = json.loads(open("/args/ESqueries.json", "r").read().replace("{{search_term}}",'""'))['search']['index']
        count=es.count(index=INDEX_NAME)['count']
        return render_template("index.html",res=res,tempVars=template_vars,count=count)
    elif request.method =='POST':
        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input"]
            print("Search Term:", search_term)
            payload = open("/args/ESqueries.json", "r").read().replace("{{search_term}}",'"'+search_term+'"')
            payload = json.dumps(json.loads(payload)["search"]["query"])
            
            INDEX_NAME = json.loads(open("/args/ESqueries.json", "r").read().replace("{{search_term}}",'""'))['search']['index']
            #url = "http://elasticsearch:9200/hacker/tutorials/_search"
            res = es.search(index=INDEX_NAME,body=payload)
            count=es.count(index=INDEX_NAME)['count']
            
            mapping=json.loads(open("/args/ESqueries.json", "r").read().replace("{{search_term}}",'""'))['search']['mapping']
            slc=[k for k,v in mapping.items()]            
            
            hits=[]

            for h in res['hits']['hits']:
              hits.append(h['_source'])

            if len(hits)<1:
              hits=pd.DataFrame(columns=slc)
              hits.loc[0]=["No results"]*len(slc)
            else:
              hits=pd.DataFrame(hits)

            hits=hits[slc]
            hits=hits.rename(columns=mapping)
            hits = hits.to_dict(orient='records')
            return render_template('index.html', hits=hits,tempVars=template_vars,count=count)
            


@app.route("/autocomplete",methods=['POST'],endpoint='autocomplete')
def autocomplete():
    if request.method == 'POST':
        search_term = request.form["input"]
        print("POST request called")
        print(search_term)
        payload = open("/args/ESqueries.json", "r").read().replace("{{search_term}}",'"'+search_term+'"')
        payload=json.dumps(json.loads(payload)["autocomplete"]["autocomplete"])
        INDEX_NAME = json.loads(open("/args/ESqueries.json", "r").read().replace("{{search_term}}",'""'))['autocomplete']['index']
        response = es.search(index=INDEX_NAME,body=payload)
        #response_dict_data = json.loads(str(response.text))
        response_dict_data = response
        return json.dumps(response_dict_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)