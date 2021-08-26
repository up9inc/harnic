import base64
import codecs
import copy
import json
from json import JSONDecodeError
from urllib.parse import urlparse, parse_qs, urlencode

from harnic.constants import JSON_INDENT, JSON_CTYPES
from harnic.utils import headers_list_to_map, is_ctype_media, is_ctype_ignored


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

        self._clean_request()
        self._clean_response()

    def _clean_request(self):
        request = self.request
        if is_ctype_media(request.get('postData', {}).get('mimeType')):
            request['raw_body'] = request['postData'].get('text')
            request['postData']['text'] = None
            return

        self._handle_request_encoding()

    def _clean_response(self):
        response = self.response
        if is_ctype_media(response.get('content', {}).get('mimeType')):
            response['raw_body'] = response['content'].get('text')
            response['content']['text'] = None
            return

        self._handle_response_encoding()

    def _handle_request_encoding(self):
        request = self.request
        post_data = request.get('postData')
        if not post_data:
            return

        if post_data.get('mimeType') in JSON_CTYPES and post_data.get('text'):
            try:
                json_object = json.loads(post_data['text'])
            except JSONDecodeError:
                pass
            else:
                json_formatted_str = json.dumps(json_object, indent=2)
                request['postData']['text'] = json_formatted_str
        elif post_data.get('encoding') == 'base64' or \
                post_data.get('comment') == 'base64':  # our tappers' custom encoding
            try:
                decoded = base64.b64decode(post_data['text'].encode('utf8'))
            except UnicodeDecodeError:
                pass
            else:
                request['raw_body'] = request['postData']['text']
                request['postData']['text'] = str(decoded, 'utf8')

    def _handle_response_encoding(self):
        response = self.response
        if response['content'].get('compressed') == "base64+gzip":  # our custom compression
            decoded = base64.b64decode(response['content']['text'])
            response['raw_body'] = response['content']['text']
            response['content']['text'] = codecs.decode(decoded, 'zlib').decode('utf-8')
        elif 'text' in response['content']:
            response['raw_body'] = response['content']['text']

        if response['content'].get('mimeType') in JSON_CTYPES and response['content'].get('text'):
            try:
                json_object = json.loads(response['content']['text'])
            except JSONDecodeError:
                pass
            else:
                json_formatted_str = json.dumps(json_object, indent=JSON_INDENT)
                response['content']['text'] = json_formatted_str

        elif response['content'].get('encoding') == "base64" \
                and response.get('raw_body') is not None and not is_ctype_ignored(response['content']['mimeType']):
            try:
                decoded = base64.b64decode(response['raw_body'])
            except UnicodeDecodeError:
                pass
            else:
                response['raw_body'] = response['content']['text']
                response['content']['text'] = str(decoded, 'utf8')
