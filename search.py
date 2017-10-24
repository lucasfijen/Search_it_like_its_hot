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
		"filter": {
			"terms": {"categorie": categories}
		},
		"query": {
			"multi_match" : {
				"query": text, 
				"fields": ["title", "accepted_answer"] 
			}
		}
	}

	return result

def search_in_index(index, text, categorie, size=1):
	res = es.search(index=index, body=make_query(text, categorie) , size=size)
	res = res['hits']['hits']
	for article in res:
		print(article['_source']['title'], article['_score'])

	print(len(res), 'results found')

start = timeit.timeit()
search_in_index('test', "material", ['3dprinting'])
print(timeit.timeit()- start)
