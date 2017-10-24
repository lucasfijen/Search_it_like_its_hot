from elasticsearch import Elasticsearch
import sys
import os
import json

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

#es.indices.create(index = 'test', body = mapping)
#es.indices.delete(index='documents_test')

for file in os.listdir('json_files'):
	with open('json_files/' + file) as data_file:    
		data = json.load(data_file)

	es.index(index='test', doc_type='document', id=data['id'], body=data)



