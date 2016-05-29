from collections import OrderedDict
from unittest import TestCase

from mock import mock

from statmouse.sqlhandler import SQLHandler


class TestSQLHandler(TestCase):
    def setUp(self):
        self._sql = mock.Mock()
        self._sqlhandler = SQLHandler(self._sql)

    def test_get_summoner_ids_set(self):
        self._sql.execute_query.return_value = [OrderedDict([('id',1)]), OrderedDict([('id',2)])]
        summoner_ids = self._sqlhandler.get_summoner_ids_set()
        self.assertEqual(summoner_ids, {1, 2})

    def test_insert_new_summoner_ids(self):
        self.fail()
