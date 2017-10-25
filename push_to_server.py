from elasticsearch import Elasticsearch
import sys
import os
import json
import time
from elasticsearch import  helpers

HOST = "http://localhost:9200/"
es = Elasticsearch(hosts=[HOST])

mapping = {
	"mapping": {
		"event": {
			"properties": {  
				"id": {"type":"string"},	
		        "answers": {"type":"string", "analyzer": "english"},
		        "comments": {"type":"string", "analyzer": "english"},
		        "answer_score": {"type":"integer"},
		        "categorie": {"type":"string", "analyzer": "english"},
		        "title": {"type":"string", "analyzer": "english"},
		        "tags": {"type":"string", "analyzer": "english"},
		        "body": {"type":"string", "analyzer": "english"},
		        "viewcount": {"type":"intger"},
		        "score": {"type":"integer"},
		        "creation_date": {"type":"date", "format": "date_time"},
		        "link": {"type":"string", "analyzer": "english"},
		        "accepted_answer": {"type":"string", "analyzer": "english"},
		        "accepted_answer_score": {"type":"integer"},
			}
		}
	}
}

es.indices.delete(index='test')
#es.indices.create(index = 'test', body = mapping)


folder = tuple(os.listdir('json_bulks'))

for bulk in folder:
	print(bulk)
	os.system("curl -s -XPOST http://localhost:9200/_bulk --data-binary @json_bulks/" + bulk)

