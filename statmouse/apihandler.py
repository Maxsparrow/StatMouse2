import requests
import json
import logging

import time

BASE_URL = 'https://na.api.pvp.net'
MATCHLIST_URI = '/api/lol/na/v2.2/matchlist/by-summoner/{summonerId}'
MATCH_URI = '/api/lol/na/v2.2/match/{matchId}'

# 500 requests per 10 minutes
# 10 requests per 10 seconds
MAX_REQUESTS = 9
PER_SECONDS = 10


class APIHandler:
    _logger = logging.getLogger(__name__)

    def __init__(self, api_key):
        self._api_key = api_key
        self._request_timestamps = []

    def _check_rate_limit(self):
        self._request_timestamps.append(time.time())
        if len(self._request_timestamps) >= MAX_REQUESTS:
            self._request_timestamps.pop(0)
            time_since_max_requests = time.time() - self._request_timestamps[0]
            if time_since_max_requests < PER_SECONDS:
                time_to_sleep = PER_SECONDS - time_since_max_requests
                self._logger.info("Waiting %.2f seconds for rate limit", time_to_sleep)
                time.sleep(time_to_sleep)

    def _get(self, uri):
        auth_params = {'api_key': self._api_key}
        self._check_rate_limit()
        response = requests.get(uri, params=auth_params)
        self._logger.debug("Getting request %s", response.url)
        if response.ok:
            return json.loads(response.content)
        else:
            self._logger.error("Status code %s: Failed to get data for url: %s" % (response.status_code, response.url))
            return {}

    def _get_summoner_matchlist(self, summoner_id):
        url = BASE_URL + MATCHLIST_URI
        built_url = url.format(summonerId=summoner_id)
        return self._get(built_url)

    def get_match_ids_from_summoner_matchlist(self, summoner_id):
        data = self._get_summoner_matchlist(summoner_id)
        if 'matches' in data:
            return [item['matchId'] for item in data['matches'] if 'matchId' in item.keys()]
        else:
            self._logger.warn("Missing matchlist data for summoner %s", summoner_id)
            return []

    def _get_match(self, match_id):
        url = BASE_URL + MATCH_URI
        built_url = url.format(matchId=match_id)
        return self._get(built_url)

    def get_summoner_ids_from_match(self, match_id):
        match = self._get_match(match_id)
        summoner_ids = []
        if 'participantIdentities' in match:
            for participant in match['participantIdentities']:
                summoner_ids.append(participant['player']['summonerId'])
            return summoner_ids
        else:
            self._logger.warn("Missing summoner data for match id %s", match_id)
            return []