from collections import OrderedDict
from unittest import TestCase

import mock as mock

from statmouse.summoners import Summoners


class TestSummoners(TestCase):
    def setUp(self):
        self._apihandler = mock.Mock()
        self._sqlhandler = mock.Mock()
        self._summoners = Summoners(self._apihandler, self._sqlhandler)

    def test_get_new_summoner_ids_no_list(self):
        with self.assertRaisesRegexp(AssertionError, "Id seeds must be a list, got <type 'int'>"):
            self._summoners.get_new_summoner_ids(1, 1)

    def test_get_new_summoner_ids(self):
        self._apihandler.get_match_ids_from_summoner_matchlist.return_value = [6, 7, 8, 9, 10]
        self._apihandler.get_summoner_ids_from_match.return_value = [11, 12, 13, 14, 15]
        self._sqlhandler.get_summoner_ids_set.return_value = {11}

        self._summoners.get_new_summoner_ids([1, 2, 3, 4, 5], 10)
        self.assertEqual(self._sqlhandler.insert_new_summoner_ids.call_args[0][0], {12, 13, 14, 15})
