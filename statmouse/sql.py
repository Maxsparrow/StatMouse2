import logging
from collections import OrderedDict

import pymysql
from pymysql.cursors import DictCursorMixin, Cursor


class OrderedDictCursor(DictCursorMixin, Cursor):
    dict_type = OrderedDict


class SQLConnection:
    _logger = logging.getLogger(__name__)

    def __init__(self, host, user, passwd, default_db=None):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._default_db = default_db
        self._logger.info("Set up SQL Connection to host %s, with user %s, and default db %s", host, user, default_db)

    def execute_query(self, query):
        self._logger.debug("Attempting to execute query: %s", query)
        conn = pymysql.connect(host=self._host,
                               user=self._user,
                               password=self._passwd,
                               db=self._default_db,
                               cursorclass=OrderedDictCursor)
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            return cur.fetchall()

if __name__ == "__main__":
    sql = SQLConnection('localhost', 'statmouse', 'rammus#1', 'statmouse')
    print sql.execute_query('select * From summoners')
