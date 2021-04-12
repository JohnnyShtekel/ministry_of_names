import connexion
import pytest
from connexion import RestyResolver
from flask_injector import FlaskInjector
from injector import Binder
from config import SWAGGER_ROOT, ELASTICSEARCH_HOST, \
    ELASTICSEARCH_PORT, ELASTIC_PROPERTIES, ELASTIC_SETTINGS, REDIS_HOST, REDIS_PORT
from providers.elasticsearch import ElasticSearchProvider, ElasticSearchFactory
from providers.redis import CacheRedisProvider, RedisSearchFactory

CITIZEN_TEST_MAPPING = {
    "mappings": {
        "citizen_test": ELASTIC_PROPERTIES
    },
    "settings": ELASTIC_SETTINGS
}


def get_redis():
    return CacheRedisProvider(
        RedisSearchFactory(
            REDIS_HOST,
            REDIS_PORT
        )
    )


def get_elasticsearch():
    return ElasticSearchProvider(
        ElasticSearchFactory(
            ELASTICSEARCH_HOST,
            ELASTICSEARCH_PORT
        ),
        "ministry_of_names_test",
        "citizen_test",
        CITIZEN_TEST_MAPPING
    )


def test_elasticsearch_configure(binder: Binder) -> Binder:
    binder.bind(
        ElasticSearchProvider,
        get_elasticsearch()
    )

    return binder


def test_redis_configure(binder: Binder) -> Binder:
    binder.bind(
        CacheRedisProvider,
        get_redis()
    )

    return binder


def clean_index() -> None:
    get_elasticsearch().delete_index()


def clean_cache() -> None:
    get_redis().clean_cache()


@pytest.fixture(autouse=True)
def test_cleaner():
    clean_index()
    clean_cache()
    yield
    clean_index()
    clean_cache()


@pytest.fixture
def test_client():
    app = connexion.App(__name__, specification_dir='../swagger')
    app.add_api(SWAGGER_ROOT, resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[ test_elasticsearch_configure, test_redis_configure])
    test_client = app.app.test_client()
    return test_client
