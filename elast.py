from elasticsearch import Elasticsearch
import json
from elasticsearch.helpers import scan
es = Elasticsearch ([{'host': '127.0.0.1', 'port': 9200}])


def insert(dictn, title):
    if dictn:
        #print(dictn)
        if es.indices.exists("threatsearch"):
            es.index(index="threatsearch", doc_type="tp", body=json.dumps(dictn), id=str(hash(title)))
        else:
            es.indices.create(index="threatsearch")
            es.index(index="threatsearch", doc_type="tp", body=json.dumps(dictn), id=str(hash(title)))

def retrieve():
    es_response = scan(
        es,
        index='capecthreats',
        doc_type='tp',
        query={"query": {"match_all": {}}}
    )

    for item in es_response:
        print(json.dumps(item))
