import unittest

from compare import har_compare
from har import HAR


class TestHarnic(unittest.TestCase):

    def test_diff(self):
        h1 = HAR('hars/e-maxx.ru/1.har')
        h2 = HAR('hars/e-maxx.ru/2.har')
        diff = har_compare(h1, h2)
        assert 1