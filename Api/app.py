import json
from pprint import pprint
from jinja2 import Environment
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import redirect

app = Flask(__name__, static_url_path='/static')
#app.jinja_env.trim_blocks = True
#app.jinja_env.lstrip_blocks = True
#env = Environment(extensions=['jinja2_ansible_filters.AnsibleCoreFiltersExtension'])
es_client = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


@app.route('/', methods=['GET', 'POST'])
def index():
    # data_list = comp_auto()
    # return render_template('index.html', results_list=jsonify(data_list))
    return render_template('index.html')


@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    if request.method == 'POST':
        print('post')
    else:
        print('get')

    json_data = request.json['variable']
    print(json_data)
    body = {
        "size": 10000,
        "query": {
            "match_all": {}
        }
    }
    es_all_response = []

    # res = es_client.search(index="capecthreats2", body=body)
    res2 = es_client.search(index="capecthreats", body=body)
    # for value in res['hits']['hits']:
    #     for key, val in value['_source'].items():
    #         if key == 'threat':
    #             v = str(val).split(':')
    #             es_all_response.append({'threat': v[1], 'value': val})
    for value in res2['hits']['hits']:
        for key, val in value['_source'].items():
            if key == 'threat':
                print(val)
                if val.find(':') == -1:
                    es_all_response.append({'threat': val, 'value': val})
                else:
                    v = str(val).split(':')
                    es_all_response.append({'threat': v[1], 'value': val})
    pprint(es_all_response)
    return jsonify(all_data=es_all_response)


@app.route('/search', methods=['GET','POST'])
def search():
    query_text = request.form.get('autocomplete')
    print(query_text)
    body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": query_text
                    }
                }
            }
        }
    }
    es_response = {}
    res = es_client.search(index="capecthreats", body=body)
    # res2 = es_client.search(index="capecthreats", body=body)
    # pprint(res2)
    # for value in res2['hits']['hits']:
    #     rese = {'values': dict(list(value['_source'].items())[1:len(value['_source'])])}
    #     es_response[value['_source']['threat']] = rese
    for value in res['hits']['hits']:
        rese = {'values': dict(list(value['_source'].items())[1:len(value['_source'])])}
        es_response[value['_source']['threat']] = rese
    # pprint(es_response)
    return render_template('result.html', es_response=es_response)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
