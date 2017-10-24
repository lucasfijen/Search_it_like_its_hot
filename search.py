import json
from elasticsearch import Elasticsearch
import pprint
import timeit

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

# q = {
# "query" : {
# 	"constant_score" : { 
# 		"filter": {
# 			"bool" : {
# 				"must" : [
# 					{"terms": {"categorie": ["3dprinting", "ai"]}}, 
# 					{"range": {"score": {"gt": 8}}}, 
# 					{"range": {"viewcount": {"gt": 1000}}},
# 				],
# 			}
# 		}
# 	},
# }
# }

def make_query(text, categories):
	result = {
	    "query": {
	        "match_all": {}
	    }
	}

	return result

def search_in_index(index, text, categorie, size=1):
	res = es.search(index=index, body=make_query(text, categorie) , size=size)
	for article in res['hits']['hits']:
		print(article['_source']['title'], article['_score'])

	print(res['hits']['total'], 'results found')

search_in_index('test', "material", ['ai'])
