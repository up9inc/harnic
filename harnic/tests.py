import unittest

from harnic.compare.matcher import create_compact_records_index, files_compare
from harnic.traffic_file import TrafficFile


class TestHarnic(unittest.TestCase):

    def test_diff(self):
        h1 = TrafficFile('hars/e-maxx.ru/1.har')
        h2 = TrafficFile('hars/e-maxx.ru/2.har')
        # h1 = TrafficFile('hars/big/1.har')
        # h2 = TrafficFile('hars/big/2.har')
        diff = files_compare(h1, h2)
        index = create_compact_records_index(diff)
        assert 1
