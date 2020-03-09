import json
import csv
from elasticsearch import Elasticsearch
import json
from elasticsearch.helpers import scan
es = Elasticsearch ([{'host': '127.0.0.1', 'port': 9200}])

csvfile = open('cve clean.csv', 'r')
#jsonfile = open('file.json', 'w')

def insert(dictn):
    if dictn:
        #print(dictn)
        if es.indices.exists("capecthreats"):
            es.index(index="capecthreats", doc_type="tp", body=json.dumps(dictn), id=dictn["threat"])
        else:
            es.indices.create(index="capecthreats")
            es.index(index="capecthreats", doc_type="tp", body=json.dumps(dictn), id=dictn["threat"])




input_file = csv.reader(csvfile)
newlist = []
dic = {}
count = 0
for row in input_file:
    print(row)
    if count < 1:
        count += 1
        continue

    dic["threat"] = row[0]
    dic["description"] = row[1]
    insert(dic)
# dic["threat"] = "CVE-2017-5754"
# dic["description"] = "Systems with microprocessors utilizing speculative execution and indirect branch prediction may allow unauthorized disclosure of information to an attacker with local user access via a side-channel analysis of the data cache."
# insert(dic)
# for rows in newlist:
#     print(rows)




print(dic)


filejson = open("cve.json", 'w')


filejson.write(json.dumps(dic, indent=2))
filejson.close()


print("Boom")








