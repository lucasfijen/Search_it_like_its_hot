import json
from elasticsearch import Elasticsearch
import pprint
import timeit

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories):
	result = {
	    "query": {
	        "bool": {
	            "must": {
	                "multi_match": {
	                    "query": text,
	                    "fields": [
	                        "title^2",
	                        "body"
	                    ]
	                }
	            },
	            "filter": {
	                "terms": {
	                    "categorie": categories
	                }
	            }
	        }
	    }
	}

	return result

def search_in_index(index, text, categorie, size=10):
	res = es.search(index=index, body=make_query(text, categorie) , size=size)
	for article in res['hits']['hits']:
		print(article['_source']['id'], article['_source']['title'], article['_score'])

	print(res['hits']['total'], 'results found')

search_in_index('test', "material", ['3dprinting', 'dba'])
