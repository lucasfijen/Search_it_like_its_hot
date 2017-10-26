import json
from elasticsearch import Elasticsearch
import pprint
import time
import pprint

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
	        "sales_over_time" : {
	            "date_histogram" : {
	                "field" : "creation_date",
	                "interval" : "month"
	            }
	        }
	    }
	}

def search_in_index(index='index', text="", categories=[], date=None, datetype=None, size=0):
	res = es.search(index = index, body = make_query(text, categories, date, datetype) , size=size)
	pprint.pprint(res)
	pprint.pprint(res['aggregations'])
	for article in res['hits']['hits']:
		print(article['_source']['categorie'])

	print(res['hits']['total'], 'results found')

	return res


search_in_index(text="material", categories=['3dprinting'], date="2017", datetype="gt")
