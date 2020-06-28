from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

app = Flask(__name__, static_url_path='/static')
CORS(app)
es_client = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [{
                    "match_all": {}
                }]
            }
        }
    }
    es_all_response = []

    res2 = es_client.search(index="threatsearch", body=body)
    if res2:
        for value in res2['hits']['hits']:
            for key, val in value['_source'].items():
                if key == "keywords":
                    val1 = ast.literal_eval(val)
                    for word in val1:
                        if word not in es_all_response:
                            es_all_response.append(word)
        return jsonify(es_all_response)
    else:
        err_res = not_found(error="no results found")
        return err_res


@app.route('/search/<search_term>', methods=['GET'])
def search(search_term):
    query_text = search_term
    body = {
        "size": 10000,
        "_source": {
            "includes": ["threat", "url", "description"],
            "excludes": ["keywords"]
        },
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": query_text
                    }
                },
                "boost": "5",
                "random_score": {},
                "boost_mode": "multiply",
                "score_mode": "max"
                }
            }
        }
    es_response = []
    res = es_client.search(index="threatsearch", body=body)
    res_keys = ["url", "description", "threat"]
    if res:
        for value in res['hits']['hits']:
            rese_dict = {}
            for key, val in value['_source'].items():
                if key in res_keys:
                    rese_dict[key] = val
            es_response.append(rese_dict)
        return jsonify(es_response)
    else:
        err_res = not_found(error="no results found")
        return err_res


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not found"+request.url}

    response = jsonify(message)
    response.status_code = 404

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
