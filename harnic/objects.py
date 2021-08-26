import base64
import codecs
import copy
from urllib.parse import urlparse, parse_qs, urlencode

from harnic.utils import headers_list_to_map, _is_ctype_ignored


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
        self._handle_encodings()

    def __repr__(self):
        return f"{self.request['method']} {self.request['url'].clean_url}"

    def _key(self):
        return self.request['method'], self.request['url'].clean_url, self.response['status']

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def _clean(self):
        request_headers = self.request.get('headers')
        if request_headers is not None:
            self.request['headers'] = headers_list_to_map(request_headers)
        response_headers = self.response.get('headers')
        if response_headers is not None:
            self.response['headers'] = headers_list_to_map(response_headers)

    def _handle_encodings(self):
        self._handle_request_encoding()
        self._handle_response_encoding()

    def _handle_request_encoding(self):
        request = self.request
        post_data = request.get('postData')
        if not post_data:
            return

        if post_data.get('encoding') == 'base64' or \
                post_data.get('comment') == 'base64':  # our tappers' custom encoding
            try:
                decoded = base64.b64decode(post_data['text'].encode('utf8'))
                request['raw_body'] = request['postData']['text']
                request['postData']['text'] = str(decoded, 'utf8')
            except UnicodeDecodeError:
                pass

    def _handle_response_encoding(self):
        response = self.response
        if response['content'].get('compressed') == "base64+gzip":  # our custom compression
            decoded = base64.b64decode(response['content']['text'])
            response['raw_body'] = codecs.decode(decoded, 'zlib').decode('utf-8')
        elif 'text' in response['content']:
            response['raw_body'] = response['content']['text']

        if response['content'].get('encoding') == "base64" \
                and response.get('raw_body') is not None and not _is_ctype_ignored(response['content']['mimeType']):
            try:
                decoded = base64.b64decode(response['raw_body'])
                response['raw_body'] = response['content']['text']
                response['content']['text'] = str(decoded, 'utf8')
            except UnicodeDecodeError:
                pass
