import base64
import codecs
import copy
import json
import os
import re
from json import JSONDecodeError
from urllib.parse import urlparse, parse_qs, urlencode

from harnic.constants import JSON_INDENT, MAX_BODY_SIZE
from harnic.utils import headers_list_to_map, is_ctype_media, is_ctype_ignored, is_ctype_json


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
        cleaned_result_url = cleaned_result_url._replace(path=self._url_patterns(self._parsed_url.path))
        return cleaned_result_url.geturl()

    def _url_patterns(self, path):
        return re.sub(r"\d{2,}", "*", path)


class Entry:

    def __init__(self, request, response, metadata):
        self.request = request
        self.response = response
        self.metadata = metadata
        self._clean()

    def __repr__(self):
        return f"{self.request['method']} {self.request['url'].clean_url}"

    def _key(self):
        status = self.response['status'] if os.getenv("HARNIC_STATUS_DIFFERENTIATES") else None
        return self.request['method'], self.request['url'].clean_url, status

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
        post_data = request.get('postData')
        if not post_data:
            return
        request['raw_body'] = request['postData'].get('text')
        if is_ctype_media(post_data.get('mimeType')) or post_data.get('size', 0) > MAX_BODY_SIZE:
            request['postData']['text'] = None
            return

        self._handle_request_types()

    def _clean_response(self):
        response = self.response
        content = response.get('content')
        if not content:
            return
        response['raw_body'] = response['content'].get('text')
        if is_ctype_media(content.get('mimeType')) or content.get('size', 0) > MAX_BODY_SIZE:
            response['content']['text'] = None
            return

        self._handle_response_types()

    def _handle_request_types(self):
        request = self.request
        post_data = request['postData']
        if post_data.get('encoding') == 'base64' or \
                post_data.get('comment') == 'base64':  # our tappers' custom encoding
            try:
                decoded = base64.b64decode(post_data['text'].encode('utf8'))
                request['postData']['text'] = str(decoded, 'utf8')
            except UnicodeDecodeError:
                pass

        if post_data.get('text') and \
                (is_ctype_json(post_data.get('mimeType')) or \
                 any(is_ctype_json(ctype) for ctype in request['headers'].get('content-type', []))):
            try:
                json_object = json.loads(post_data['text'])
            except JSONDecodeError:
                pass
            else:
                json_formatted_str = json.dumps(json_object, indent=2)
                request['postData']['text'] = json_formatted_str

    def _handle_response_types(self):
        response = self.response
        content = response['content']
        if content.get('compressed') == "base64+gzip":  # our custom compression
            decoded = base64.b64decode(content['text'])
            response['content']['text'] = codecs.decode(decoded, 'zlib').decode('utf-8')
        elif content.get('encoding') == "base64" \
                and content.get('text') is not None \
                and not is_ctype_ignored(content['mimeType']):
            try:
                decoded = base64.b64decode(content['text'])
                content['text'] = str(decoded, 'utf8')
            except UnicodeDecodeError:
                pass

        if content.get('text') and \
                (is_ctype_json(content.get('mimeType')) or \
                 any(is_ctype_json(ctype) for ctype in response['headers'].get('content-type', []))):
            try:
                json_object = json.loads(response['content']['text'])
            except JSONDecodeError:
                pass
            else:
                json_formatted_str = json.dumps(json_object, indent=JSON_INDENT)
                response['content']['text'] = json_formatted_str
