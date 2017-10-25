import json
from elasticsearch import Elasticsearch
import pprint
import time
import pprint

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories):
	question = {
	"multi_match":{
		"query": text,
		"fields" : [
                "title^2",
                "body"
				]
	}},

	question_filter = {
	"bool": {
		"filter": {
			"bool": {
				"must": [
					{"range": {"score": {"gt": 8}}}, 
						{"terms": {"categorie": categories}}]}}}}

	print(question[0])
	print(question_filter)
	result = {"query": question[0] + question_filter}
	return result

def search_in_index(index, text, categorie, size=10):
	res = es.search(index = index, body = make_query(text, categorie) , size=size)
	for article in res['hits']['hits']:
		print(article['_source']['title'])

	print(res['hits']['total'], 'results found')

	return res

# start = time.time()
search_in_index('test', "material", ['3dprinting'])
# end = time.time()

# print(end - start)

		        # "bool": {
		        #     "must": {
		        #         "multi_match": {
		        #             "query": text,
		        #             "fields": [
		        #                 "title^2",
		        #                 "body"
		        #             ]
		        #         }
		        #     },
		        #    	"filter": {
		        #    		"bool":{
		        #    			"must":	[
			       #     			{"range": {"score": {"gt": 8}}},
			       #     			{"terms": {"categorie": categories}}
		        #    			]
		        #     	}
		        #     },
		        # }