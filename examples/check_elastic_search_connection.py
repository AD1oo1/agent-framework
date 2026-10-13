import os
from pathlib import Path

from elasticsearch import Elasticsearch


password = os.environ["ELASTIC_PASSWORD"]

certificate_path = Path("http_ca.crt")

client = Elasticsearch(
    "https://localhost:9200",
    ca_certs=str(certificate_path),
    basic_auth=("elastic", password),
)

info = client.info()

print("Connected to Elasticsearch!")
print(f"Cluster: {info['cluster_name']}")
print(f"Version: {info['version']['number']}")
