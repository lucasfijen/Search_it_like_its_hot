import json
from elasticsearch import Elasticsearch
import pprint
import time
import pprint
import datetime

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories, date, datetype):
	if len(date) == 4:
		date = datetime.datetime.strptime(date, "%Y")
	
	fields = ["title^2", "body", "accepted_answer", "answers", "comments"]
	query = {}
	query['bool'] = {"filter": {"bool": {"must": []}}}

	if len(categories) > 0:
		query["bool"]["filter"]["bool"]["must"].append({"terms": {"categorie": categories}}) 

	if date and datetype:
		query["bool"]["filter"]["bool"]["must"].append({"range": {"creation_date": {datetype: date}}}) 

	query["bool"]['must'] = {"multi_match": {"fields": fields, "query": text}}

	aggs =	{
	        "hits_over_time" : {
	            "date_histogram" : {
	                "field" : "creation_date",
	                "interval" : "month"
	            }
	        }
	    }

	return {"query": query, 'aggs': aggs}

def search_in_index(index='index', text="", categories=[], date=None, datetype=None, size=10):
	res = es.search(index = index, body = make_query(text, categories, date, datetype) , size=size)
	for article in res['hits']['hits']:
		print(article['_source']['title'])

	print(res['hits']['total'], 'results found')
	#pprint.pprint(res['aggregations'])
	
	return res

def get_all_categories():
	query = {
	    "aggs" : {
	        "genres" : {
	            "terms" : { "field" : "categorie" }
	        }
	    }
	}
	res = es.search(index = 'index', body = query, size=0)

	result = []
	for categorie in res['aggregations']['genres']['buckets']:
		result.append(categorie['key'])

	return result





#search_in_index(text="material", categories=['3dprinting'], date="2017", datetype="gt")
print(get_all_categories())
