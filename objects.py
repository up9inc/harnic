import copy
from urllib.parse import urlparse, parse_qs, urlencode

from comparisons import dict_compare, headers_list_to_map


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
        self._clean()

    def __repr__(self):
        return f"{self.request['method']} {self.request['url'].clean_url}"

    def _key(self):
        return self.request['method'], self.request['url'].clean_url

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def _clean(self):
        request_headers = self.request.get('headers')
        if request_headers:
            self.request['headers'] = headers_list_to_map(request_headers)
        response_headers = self.response.get('headers')
        if response_headers:
            self.response['headers'] = headers_list_to_map(response_headers)


# TODO: this may be a func?
class EntryDiff:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.equal = None
        self.fields = self._get_diff()

    @property
    def query_params(self):
        return dict_compare(a.request['url'].query_params)

    def _get_diff(self):
        # method and url are not handled here as long as they are part of the entry hash
        fields = {'request': {}, 'response': {}}

        qs_cmp = dict_compare(self.a.request['url'].query_params,
                              self.b.request['url'].query_params)
        headers_cmp = dict_compare(self.a.request['headers'],
                                   self.b.request['headers'])
        fields['request']['query_params'] = qs_cmp
        fields['request']['headers'] = headers_cmp

        self.equal = all(c.equal for c in [qs_cmp, headers_cmp])
        return fields
