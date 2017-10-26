import json
from elasticsearch import Elasticsearch
import pprint
import time
import pprint
import numpy as np
import matplotlib.pyplot as plt

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories, date, datetype):

	return {
		"query":{
			"bool":{
				"filter":{"term": {"categorie": "3dprinting"}}
			}
		},
	    "aggs" : {
	        "hits_over_time" : {
	            "date_histogram" : {
	                "field" : "creation_date",
	                "interval" : "month"
	            }
	        }
	    }
	}

def search_in_index(index='index', text="", categories=[], date=None, datetype=None, size=0):
	res = es.search(index = index, body = make_query(text, categories, date, datetype) , size=size)
	#pprint.pprint(res)
	print_histo_values(res['aggregations'])
	for article in res['hits']['hits']:
		print(article['_source']['categorie'])

	print(res['hits']['total'], 'results found')

	return res

def print_histo_values(aggs):
	aggs = aggs['hits_over_time']['buckets']
	x = []
	y = []
	for month in aggs:
		x.append(month['key_as_string'][:-9])
		y.append(month['doc_count'])

	objects = x
	y_pos = np.arange(len(objects))
	performance = y
	 
	plt.bar(y_pos, performance, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Usage')
	plt.title('Programming language usage')
	 
	plt.show()

search_in_index(text="material", categories=['3dprinting'], date="2017", datetype="gt")


