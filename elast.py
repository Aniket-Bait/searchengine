from elasticsearch import Elasticsearch
import json
from elasticsearch.helpers import scan
es = Elasticsearch ([{'host': '192.168.1.4', 'port': 9200}])

def insert(dictn):

    if dictn:
        print(dictn)
        if es.indices.exists("capecthreats"):
            es.index(index="capecthreats", doc_type="tp", body=json.dumps(dictn))
        else:
            es.indices.create(index="capecthreats")
            es.index(index="capecthreats", doc_type="tp", body=json.dumps(dictn))

def retrieve():
    es_response = scan(
        es,
        index='capecthreats',
        doc_type='tp',
        query={"query": {"match_all": {}}}
    )

    for item in es_response:
        print(json.dumps(item))
