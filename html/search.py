import json
from elasticsearch import Elasticsearch
import pprint
import time
import pprint
import datetime

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories, date, datetype):
	try:
		if len(date) == 4:
			date = datetime.datetime.strptime(date, "%Y")
	except:
		pass


	fields = ["title^2", "body", "accepted_answer", "answers", "comments"]
	query = {}
	query['bool'] = {"filter": {"bool": {"must": []}}}

	query["bool"]["filter"]["bool"]["must"].append({"terms": {"categorie": categories}})

	if date and datetype:
		query["bool"]["filter"]["bool"]["must"].append({"range": {"creation_date": {datetype: date}}})

	query["bool"]['must'] = {"multi_match": {"fields": fields, "type": "best_fields","query": text}}

	aggs =	{
	        "hits_over_time" : {
	            "date_histogram" : {
	                "field" : "creation_date",
	                "interval" : "month"
	            }
	        }
	    }
	function = [{
		"field_value_factor": {
			"field": "score",
			"factor": 0.01,
			}
	}]

	return {"explain": True, "query":{"function_score": {"query": query, "functions": function, "boost_mode": "sum"}}}

def search_in_index(text="", categories=[], date=None, datetype=None, size=1):
	query = make_query(text, categories, date, datetype)
	res = es.search(index = 'index', body = query , size=size)

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


