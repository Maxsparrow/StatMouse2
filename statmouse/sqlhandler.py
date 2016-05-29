import logging
from jinja2 import Environment, PackageLoader


class SQLHandler:
    _logger = logging.getLogger(__name__)

    def __init__(self, sql):
        self._sql = sql
        self._env = Environment(loader=PackageLoader('statmouse', 'templates'))

    def get_summoner_ids_set(self, limit=None):
        """
        :param limit: limit number of summoner ids
        :type limit: int
        :return: unique set of summoner ids
        :rtype: set
        """
        query = "SELECT id FROM summoners"
        if limit:
            query += " LIMIT %s" % limit
        results = self._sql.execute_query(query)
        return set([result['id'] for result in results])

    def insert_new_summoner_ids(self, new_ids):
        """
        :param new_ids:
        :type new_ids: set
        :return:
        """
        template = self._env.get_template('insert_into.sql')
        list_of_dicts = [{'id': new_id} for new_id in new_ids]
        query = template.render(destination='summoners', rows=list_of_dicts)
        self._sql.execute_query(query)

