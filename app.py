import logging
from logging.config import fileConfig
import connexion
from flask_cors import CORS
from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver
from config import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX, ELASTICSEARCH_DOC_TYPE, CITIZEN_MAPPING, \
    SWAGGER_ROOT, SERVICE_PORT, REDIS_PORT, REDIS_HOST
from providers.elasticsearch import ElasticSearchFactory, ElasticSearchProvider
from providers.redis import CacheRedisProvider, RedisSearchFactory


def redis_configure(binder: Binder) -> Binder:
    binder.bind(
        CacheRedisProvider,
        CacheRedisProvider(
            RedisSearchFactory(
                REDIS_HOST,
                REDIS_PORT
            ),
        )
    )

    return binder



def elasticsearch_configure(binder: Binder) -> Binder:
    binder.bind(
        ElasticSearchProvider,
        ElasticSearchProvider(
            ElasticSearchFactory(
                ELASTICSEARCH_HOST,
                ELASTICSEARCH_PORT
            ),
            ELASTICSEARCH_INDEX,
            ELASTICSEARCH_DOC_TYPE,
            CITIZEN_MAPPING
        )
    )

    return binder


def create_app(configures):
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api(SWAGGER_ROOT, resolver=RestyResolver('api'))
    CORS(app=app.app)
    fileConfig('logger.ini')
    FlaskInjector(app=app.app, modules=configures)
    return app


app = create_app([elasticsearch_configure, redis_configure])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)
