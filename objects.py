import copy
from urllib.parse import urlparse, parse_qs, urlencode


class Url:

    def __init__(self, url):
        self.url = url
        self._parsed_url = urlparse(self.url)
        self.query_params = {}
        self.clean_url = self._get_clean_url()

    def __repr__(self):
        return self.clean_url

    def _get_clean_url(self):
        self.query_params = parse_qs(self._parsed_url.query)
        cleaned_qparams = {k: "%s" % k for k in self.query_params.keys()}
        cleaned_query = urlencode(cleaned_qparams)
        cleaned_result_url = copy.copy(self._parsed_url)
        cleaned_result_url = cleaned_result_url._replace(query=cleaned_query)
        return cleaned_result_url.geturl()


class Entry:

    def __init__(self, request, response, metadata):
        self.request = request
        self.response = response
        self.metadata = metadata

    def __repr__(self):
        return f"{self.request['method']} {self.request['url'].clean_url}"

    def _key(self):
        return self.request['method'], self.request['url'].clean_url

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        return hash(self) == hash(other)


# TODO: this may be a func?
class EntryDiff:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.diff = self._get_diff()

    def _get_diff(self):
        pass
