from elasticsearch import Elasticsearch
import json
import pprint
import datetime

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

def make_query(text, categories, exclude, date, datetype):
	# convert date to datetime object
	try:
		if len(date) == 4:
			if datetype == 'in':
				second_date = str(int(date) + 1)
				second_date = datetime.datetime.strptime(second_date, "%Y")
			date = datetime.datetime.strptime(date, "%Y")

	except:
		pass


	fields = ["title^2", "body", "accepted_answer", "answers", "comments^0.5"]
	query = {}
	query['bool'] = {"filter": {"bool": {"must": []}}}

	# add categorie filter
	query["bool"]["filter"]["bool"]["must"].append({"terms": 
						{"categorie": categories}})

	# add date filter
	if datetype == 'in':
		query["bool"]["filter"]["bool"]["must"].append({"range": 
						{"creation_date": {'gte': date, 'lt': second_date}}})
	elif date and datetype:
		query["bool"]["filter"]["bool"]["must"].append({"range": 
						{"creation_date": {datetype: date}}})

	# add text filter
	query["bool"]['must'] = {"multi_match": {"fields": fields, 
						"type": "best_fields","query": text}}

	# make aggregation
	aggs =	{
	        "hits_over_time" : {
	            "date_histogram" : {
	                "field" : "creation_date",
	                "interval" : "month"
	            }
	        },
	        "found_categories":{
	        		"terms": {"field": "categorie", "size": 1000}
	        }
	    }

	# add function
	function = [{
		"field_value_factor": {
			"field": "score",
			"factor": 0.1,
			}
	}]

	# return query
	return {"explain": True, "query":{"function_score": {"functions": function, 
			"query": query, "boost_mode": "sum", "max_boost":2}}, "aggs":aggs}

def search_in_index(text="", categories=[], exclude=[], date=None, 
						datetype=None, size=1):
	
	# make query from imput.
	query = make_query(text, categories, exclude, date, datetype)

	# search for the query in the index
	res = es.search(index = 'index', body = query , size=size)

	# return results
	return res 

def get_all_categories():
	query = {
	    "aggs" : {
	        "genres" : {
	            "terms" : { "field" : "categorie", 'size': 1000 }
	        }
	    }
	}
	res = es.search(index = 'index', body = query, size=0)

	result = [categorie['key'] for categorie in 
							res['aggregations']['genres']['buckets']]

	return result
