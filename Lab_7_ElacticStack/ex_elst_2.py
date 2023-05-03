from elasticsearch import Elasticsearch
from pprint import pprint
es_host = Elasticsearch("http://192.168.4.54:9200/")

res = es_host.search(index=".ds-filebeat*", body={"query": {"match_all": {}}})
print("Hits Total: " + str(res['hits']['total']['value']))