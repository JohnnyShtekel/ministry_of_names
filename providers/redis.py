from datetime import datetime
from typing import Iterator

from redis import StrictRedis

from providers.provider_factory_base import ProviderFactoryBase


class RedisSearchFactory(ProviderFactoryBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    def create(self) -> StrictRedis:
        return StrictRedis(host=self.host, port=self.port)


class CacheRedisProvider(object):
    def __init__(
            self,
            redis_factory: ProviderFactoryBase
    ):
        """
        :param redis client factory:
        """
        self.elastic_factory = redis_factory
        self.instance = None

    def _connection(self) -> StrictRedis:
        if not self.instance:
            self.instance = self.elastic_factory.create()
        return self.instance

    def cache_all_similar_names(self, similar_collection: Iterator) -> None:
        for first_name in similar_collection:
            self.set(first_name)

    def exists(self, key) -> bool:
        return self._connection().exists(key)

    def set(self, key) -> None:
        self._connection().set(key, str(datetime.now()))

    def clean_cache(self):
        self._connection().flushall()
