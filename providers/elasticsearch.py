from typing import Iterator
from elasticsearch import Elasticsearch
from providers.provider_factory_base import ProviderFactoryBase


class ElasticSearchFactory(ProviderFactoryBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    def create(self) -> Elasticsearch:
        return Elasticsearch(
            [{'host': self.host, 'port': self.port}]
        )


class ElasticSearchProvider(object):
    def __init__(
            self,
            elastic_factory: ProviderFactoryBase,
            index_name: str,
            doc_type: str,
            index_mapper: dict
    ):
        """
        It creates the index if it doesn't exists
        :param elasticsearch:
        :param index_name:
        :param doc_type:
        :param index_mapper:
        """
        self.index_name = index_name
        self.index_mapper = index_mapper
        self.doc_type = doc_type
        self.elastic_factory = elastic_factory
        self.instance = None

    def _connection(self) -> Elasticsearch:
        if not self.instance:
            self.instance = self.elastic_factory.create()
            if not self.instance.indices.exists(self.index_name):
                self.instance.indices.create(
                    index=self.index_name,
                    body=self.index_mapper,
                    params={"include_type_name": "true"}
                )

        return self.instance

    def index(self, payload: dict, doc_id: str) -> bool:
        return self._connection().index(
            index=self.index_name,
            doc_type=self.doc_type,
            body=payload,
            id=doc_id
        )

    def delete_index(self):
        return self._connection().indices.delete(
            index=self.index_name,  ignore=[400, 404]
        )

    def exists(self, doc_id: str):
        return self._connection().exists(
            index=self.index_name,
            doc_type=self.doc_type,
            id=doc_id
        )

    def bulk_exists(self, doc_id: str):
        return self._connection().exists(
            index=self.index_name,
            doc_type=self.doc_type,
            id=doc_id
        )

    def similar(self, name: str) -> bool:
        matches = self._connection().search(
            index=self.index_name,
            doc_type=self.doc_type,
            body={
                'query': {
                    "bool": {
                        "must": [{
                            'match': {
                                'first_name': {
                                    "query": name,
                                    "fuzziness": "1"
                                },
                            }
                        }]
                    }
                }

            })

        hits = matches['hits']['hits']
        if hits:
            return True

        return False

    def search_by_prefix(self, name: str) -> Iterator:
        matches = self._connection().search(
            index=self.index_name,
            doc_type=self.doc_type,
            body={
                "size": 100,
                "query": {
                    "prefix": {"first_name": name}
                }
            })

        hits = map(lambda x: x["_source"], matches['hits']['hits'])

        return hits
