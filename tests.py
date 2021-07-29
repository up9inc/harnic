import unittest

from har import HAR


class TestHarnic(unittest.TestCase):

    def test_diff(self):
        h1 = HAR('hars/e-maxx.ru/1.har')
        h2 = HAR('hars/e-maxx.ru/2.har')
        diff = h1.compare(h2)
        diff.get_opcodes()
        assert 1
