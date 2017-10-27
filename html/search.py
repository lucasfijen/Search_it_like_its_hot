import json
from elasticsearch import Elasticsearch
import pprint
import time
import pprint
import datetime

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories, exclude, date, datetype):
	try:
		if len(date) == 4:
			if datetype == 'in':
				second_date = str(int(date) + 1)
				second_date = datetime.datetime.strptime(second_date, "%Y")
			date = datetime.datetime.strptime(date, "%Y")

	except:
		pass


	fields = ["title", "body", "accepted_answer", "answers", "comments"]
	query = {'bool':{'filter':{'bool':{}}, 'must':{}}}

	must = []
	must.append({"terms": {"categorie": categories}})

	if datetype == 'in':
		must.append({"range": {"creation_date": {'gte': date, 'lt': second_date}}})

	elif date and datetype:
		must.append({"range": {"creation_date": {datetype: date}}})

	query["bool"]['must'] = {"multi_match": {"fields": fields, "type": "most_fields","query": text}}

	must_not = []

	for field in fields:
		print(exclude)
		must_not.append({"terms": {field: exclude}})

	query['bool']['filter']['bool'] = {'must':must, 'must_not':must_not}

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

	return {"explain": True, "query":{"function_score": {"functions": function, "query": query, "boost_mode": "sum"}}, "aggs":aggs}

def search_in_index(text="", categories=[], exclude=[], date=None, datetype=None, size=1):
	query = make_query(text, categories, exclude, date, datetype)
	print(query)
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
