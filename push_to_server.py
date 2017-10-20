import sys
import json
from elasticsearch import Elasticsearch

HOST = 'http://localhost:9200/'
es = Elasticsearch(hosts=[HOST])

# mapping =	{
# 	'mapping': {
# 		'post': {
# 			'properties': {  
# 				"id": {"type":"string"},	
# 		        "answers": {"type":"string", "analyzer": "english"},
# 		        "comments": {"type":"string", "analyzer": "english"},
# 		        "answer_score": {"type":"integer"},
# 		        "categorie": {"type":"string", "analyzer": "english"},
# 		        "title": {"type":"string", "analyzer": "english"},
# 		        "tags": {"type":"string", "analyzer": "english"},
# 		        "body": {"type":"string", "analyzer": "english"},
# 		        "viewcount": {"type":"intger"},
# 		        "score": {"type":"integer"},
# 		        "creation_date": {"type":"date", "format": "date_time"},
# 		        "link": {"type":"string", "analyzer": "english"},
# 		        "accepted_answer": {"type":"string", "analyzer": "english"},
# 		        "accepted_answer_score": {"type":"integer"},
# 			}
# 		}
# 	}
# }

# es.indices.create(index='documents_test', body=mapping)
#es.indices.delete(index=)

print('mapping done')

docs = [
  	{
  		"id": "3dprinting1",
        "answers": "",
        "comments": "Did I just place the first upvote Congrats on getting this site off the ground!What are you looking for in an answer You are basically asking how to make your car drive faster while using less fuel.@TomvanderZanden I'd heard of some experiments in the past that have two nozzles one larger and one finer The fine detail would take two passes two layers to build up the needed high resolution exterior while the larger nozzle would perform the infill with only one layer for every two high resolution layers and could do so very quickly due to the nozzle size and the amount of plastic it could pump I haven't heard anything more and I expect there are other methods that could speed this up by now this was years ago ",
        "answer_score": 0,
        "categorie": "3dprinting",
        "title": "How to obtain high resolution prints in a shorter period of time?",
        "tags": "",
        "body": " When I've printed an object I've had to choose between high resolution and quick prints What techniques or technologies can I use or deploy to speed up my high resolution prints ",
        "viewcount": 135,
        "score": 8,
        "creation_date": "2016-01-12T18:45:19.963",
        "link": "3dprinting.stackexchange.com/questions/1/How-to-obtain-high-resolution-prints-in-a-shorter-period-of-time?",
        "accepted_answer": " You could experiment with slicing For example you might not need high resolution all over the object but you can speed up some straight parts by using greater layer high there See a part of Slic3r manual about such thing It is also possible to print thicker infill every Nth layer see Infill optimization in Slic3r Other slicers might have those features as well ",
        "accepted_answer_score": 7
    },
] 
# for doc in docs:
# 	es.index(index='documents_test', doc_type='document', id=doc['id'], body=doc)

query = "you"
q = {"query": {"query_string": {"query" : query}}}
res = es.search(index='documents_test', body=q, size=100)
print(res['hits']['hits'][0]['_source'])