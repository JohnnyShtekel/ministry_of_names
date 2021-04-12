import logging
from typing import Tuple, Dict
from flask_injector import inject
from api.exception import RegisterCitizenNotAllowedError, RegisterCitizenError
from config import K_DISTANCE, ALPHABET
from providers.elasticsearch import ElasticSearchProvider
from flask import request
from providers.redis import CacheRedisProvider
from utils import hamming_circle

logger = logging.getLogger(__name__)


class Citizen(object):
    @inject
    def post(self, es: ElasticSearchProvider, cache: CacheRedisProvider, citizen: dict) -> Tuple[Dict[str, str], int]:
        """
        This wil return a register the citizen if his first name not exists
        or his first name is one edit distance.
        """

        first_name = citizen['first_name'].lower()

        try:
            if self._is_eligible_for_registration(es, cache, first_name):
                raise RegisterCitizenNotAllowedError()

            if not self._register_citizen(es, citizen, first_name):
                raise RegisterCitizenError()

            self._cache_similar_names(cache, first_name)

            msg = f"citizen {first_name} registered"

            logger.info(msg)

            return {"message": msg}, 201

        except RegisterCitizenNotAllowedError:
            error_msg = f"the name {first_name} is similar up to one editing distance"
            logger.error(error_msg)
            return {"error": error_msg}, 409

        except RegisterCitizenError:
            error_msg = f"Failed to register citizen {first_name}"
            logger.error(error_msg)
            return {"error": error_msg}, 400

        except Exception as ex:
            error_msg = f"unhandled error in register citizen {first_name}"
            logger.error(error_msg, ex)
            return {"error": error_msg + str(ex)}, 500

    @inject
    def get(self, es: ElasticSearchProvider) -> Tuple[Dict, int]:
        """
        search for prefix by first_name
        """
        first_name = request.args.get('first_name').lower()

        try:
            hits = es.search_by_prefix(first_name)
            return {"citizens": list(hits)}, 200

        except Exception as ex:
            error_msg = f"unhandled error for search citizen {first_name}"
            logger.error(error_msg, ex)
            return {"error": error_msg}, 500

    @staticmethod
    def _is_eligible_for_registration(es: ElasticSearchProvider, cache: CacheRedisProvider, first_name: str) -> bool:

        if cache.exists(first_name) or es.similar(first_name) or es.exists(first_name):
            return True

        else:
            permutations = hamming_circle(first_name, K_DISTANCE, ALPHABET)

            for permutation in permutations:
                if es.exists(permutation):
                    return True

            return False

    @staticmethod
    def _register_citizen(es: ElasticSearchProvider, citizen: dict, first_name: str) -> bool:
        return es.index(citizen, doc_id=first_name)

    @staticmethod
    def _cache_similar_names(cache: CacheRedisProvider, first_name: str):
        permutations = hamming_circle(first_name, K_DISTANCE, ALPHABET)
        cache.cache_all_similar_names(permutations)


class_instance = Citizen()
