import unittest

from harnic.compare import har_compare
from harnic.compare.har import create_compact_records_index
from harnic.har import HAR


class TestHarnic(unittest.TestCase):

    def test_diff(self):
        h1 = HAR('hars/e-maxx.ru/1.har')
        h2 = HAR('hars/e-maxx.ru/2.har')
        diff = har_compare(h1, h2)
        index = create_compact_records_index(diff)
        assert 1
