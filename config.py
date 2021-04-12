import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SWAGGER_ROOT = os.path.join(PROJECT_ROOT, "swagger", "citizen.yaml")
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT', 9200)
ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', "localhost")
SERVICE_PORT = os.environ.get('SERVICE_PORT', 5000)
ELASTICSEARCH_INDEX = 'ministry_of_names'
ELASTICSEARCH_DOC_TYPE = 'citizen'
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
K_DISTANCE = 1


ELASTIC_SETTINGS = {
        "analysis": {
            "analyzer": {
                "lowercase": {
                    "tokenizer": "keyword",
                    "filter": ["lowercase"]
                }
            }
        },
        "number_of_shards": 3,
        "number_of_replicas": 2
}

ELASTIC_PROPERTIES = {
            "properties": {
                "first_name": {
                    "type": "text",
                    "analyzer": "lowercase",
                },
                "last_name": {
                    "type": "text"
                }
            }
        }


CITIZEN_MAPPING = {
    "mappings": {
        "citizen": ELASTIC_PROPERTIES
    },
    "settings": ELASTIC_SETTINGS
}
