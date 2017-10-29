from elasticsearch import Elasticsearch
import sys
import os
from elasticsearch import  helpers
import json

# connect the the host
HOST = "http://localhost:9200/"
es = Elasticsearch(hosts=[HOST])

# create request_body
request_body = {
    "settings" : {
        "number_of_shards": 5,
        "number_of_replicas": 0
    }
}

# create mapping
mapping = {
		"document": {
			"properties": {
				"id": {"type":"string"},
				"title": {"type":"string", "analyzer": "english"},
				"body": {"type":"string", "analyzer": "english"},
				"categorie": {"type":"keyword"},
		        "viewcount": {"type":"integer"},
		        "score": {"type":"integer"},
		        "creation_date": {"type":"date", "format": "date_hour_minute_second"},
		        "answers": {"type":"string", "analyzer": "english"},
		        "comments": {"type":"string", "analyzer": "english"},
		        "answer_score": {"type":"integer"},
		        "accepted_answer": {"type":"string", "analyzer": "english"},
		        "accepted_answer_score": {"type":"integer"},
		        "link": {"type":"string", "analyzer": "english"},
			}
		}
	}

# delete index if there is any
try:
	es.indices.delete(index='index')
except:
	pass

# create index and add mapping to it
es.indices.create(index = 'index', body = request_body)
es.indices.put_mapping(index="index", doc_type="document", body=mapping)


folder = tuple(os.listdir('json_bulks'))

# add all bulks to elasticsearch
for bulk in folder:
	print(bulk)
	os.system("curl -s -XPOST http://localhost:9200/_bulk --data-binary @json_bulks/" + bulk)
