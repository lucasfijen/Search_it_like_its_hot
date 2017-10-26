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

def search_in_index(index='index', text="", categories=[], date=None, datetype=None, size=1):
	res = es.search(index = index, body = make_query(text, categories, date, datetype) , size=size)
	# pprint.pprint(res)
	print_histo_values(res)
	# for article in res['hits']['hits']:
	# 	print(article['_source']['categorie'])

	print(res['hits']['total'], 'results found')

	return res

def print_histo_values(res):
	title = "Timeline" 
	data = res['aggregations']['hits_over_time']['buckets']

	titel = "dit moet een mooie titel worden"
	result = '''<script type="text/javascript">
	function make_graph() {
	var chart = new CanvasJS.Chart("chartContainer",
	{
		title:{
		text:\"'''
	result += title
	result += '''\"},
		data: [
			{
			color: 'blue',
			dataPoints: ['''
	for line in data:
		result += "{label:" + "\"" + line['key_as_string'][:-12] + "\", y:" + str(line['doc_count']) + '},'
	result += ''']
				}
			]
		});

		chart.render();
		}
		make_graph()
	 </script>'''

	return result

search_in_index(text="material", categories=['3dprinting'], date="2017", datetype="gt")
