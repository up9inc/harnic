import unittest

from termcolor import colored

from harnic.compare import har_compare
from harnic.compare.matcher import create_compact_records_index
from harnic.traffic_file import TrafficFile
from harnic.schemas import HarSchema


class TestHarnic(unittest.TestCase):

    def test_diff(self):
        h1 = TrafficFile('hars/e-maxx.ru/1.har')
        h2 = TrafficFile('hars/e-maxx.ru/2.har')
        diff = har_compare(h1, h2)
        index = create_compact_records_index(diff)
        assert 1
