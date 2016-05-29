import logging
import random

from statmouse.apihandler import APIHandler
from statmouse.sqlhandler import SQLHandler


class Summoners:
    _logger = logging.getLogger(__name__)

    def __init__(self, apihandler, sqlhandler, max_insert_amount=100):
        """
        :param apihandler:
        :param sqlhandler:
        :type apihandler: APIHandler
        :type sqlhandler: SQLHandler
        """
        self._apihandler = apihandler
        self._sqlhandler = sqlhandler
        self._max_insert_amount = max_insert_amount
        self._new_ids = set()
        self._existing_ids = set()

    def get_new_summoner_ids(self, id_seeds=None, amount=100):
        assert isinstance(id_seeds, list) or id_seeds is None, "Id seeds must be a list, got %s" % type(id_seeds)
        self._logger.info("Attempting to get %s new summoner ids with seeds %s", amount, id_seeds)

        self._existing_ids = self._sqlhandler.get_summoner_ids_set()
        self._logger.info("Found %s existing summoner ids in database", len(self._existing_ids))

        if not id_seeds:
            shuffled = list(self._existing_ids)
            random.shuffle(shuffled)
            # Don't need to use all the ids
            id_seeds = shuffled[:amount]

        self._get_new_ids(id_seeds, amount)

    def _get_new_ids(self, id_seeds, amount):
        self._saved_id_count = 0
        random.shuffle(id_seeds)
        for id_seed in id_seeds:
            match_ids = self._apihandler.get_match_ids_from_summoner_matchlist(id_seed)
            for match_id in match_ids:
                summoner_ids = self._apihandler.get_summoner_ids_from_match(match_id)
                for summoner_id in summoner_ids:
                    if summoner_id not in self._existing_ids:
                        self._new_ids.add(summoner_id)
                if len(self._new_ids) >= amount or len(self._new_ids) >= self._max_insert_amount:
                    self._save_summoner_ids()

    def _save_summoner_ids(self):
        self._sqlhandler.insert_new_summoner_ids(self._new_ids)
        self._saved_id_count += len(self._new_ids)
        self._existing_ids = self._existing_ids.union(self._new_ids)
        self._new_ids = set()
