import json
import logging
import traceback
from urllib.parse import urlencode

import dateutil.parser

from objects import Url, Entry

logging = logging.getLogger(__name__)


def load(fname):
    with open(fname, 'r') as f:
        loads = json.load(f)

    if isinstance(loads, dict):
        for page in loads['log'].get('pages', ()):  # fix stupid Firefox non-conforming to HAR spec
            page.setdefault('title', page['id'])

        entries = loads['log']['entries']
        source = loads.get('log', {}).get('creator', {}).get("_source", None)
    else:
        entries = loads
        source = None

    logging.debug("Entries in HAR: %s", len(entries))
    metainfo = {'_source': source}
    return _har_entry_reader(entries, metainfo)


def _har_entry_reader(entries, metadata):
    for entry in entries:
        try:
            if metadata.get('messageType') == 'kafka':
                req, resp = _from_kafka_msg(entry)
            else:
                req, resp = _process_entry(entry)
        except BaseException:
            logging.warning("Failed to process entry: %s", traceback.format_exc())
            continue

        yield Entry(**{
            "request": req,
            "response": resp,
            "metadata": metadata
        })

    if 'fd' in metadata:  # TODO: not really guaranteed to close fd...
        metadata['fd'].close()


def _from_kafka_msg(entry):
    req = {
        '_ts': entry['timestamp'] / 1000,
        'url': 'kafka://kafka/' + entry['topic'],
        'headers': [{"name": x, "value": y} for x, y in entry['headers'].items()] if entry['headers'] else [],
        'cookies': [],
        'method': "PUT",
        'postData': {"text": entry['value'], 'mimeType': ''}
    }

    if entry['key'] is not None:
        req['url'] += '?' + urlencode({"key": entry['key']})

    resp = {
        '_ts': entry['timestamp'] / 1000,
        'headers': [],
        'status': 202,  # kafka always accepts the message
        'content': {}
    }
    return req, resp


def _process_entry(entry):
    _parse_and_add_cookies_in_entry(entry)
    req = entry['request']
    for k in list(req.keys()):
        if k not in ('method', 'url', 'headers', 'cookies', 'queryString', 'bodySize', 'postData', '_ts'):
            req.pop(k)
            if not k.startswith('_') and k not in ('httpVersion', 'headersSize', 'comment'):
                logging.debug("Dropped key: %s", k)
    resp = entry['response']
    for k in list(resp.keys()):
        if k not in ('status', 'headers', 'cookies', 'content', '_ts'):
            resp.pop(k)
            if not k.startswith('_') and k not in ('statusText', 'httpVersion', 'headersSize', 'redirectURL',
                                                   'comment', 'bodySize'):
                logging.debug("Dropped key: %s", k)

    if 'url' in req:
        req['url'] = Url(req['url'])

    if '_ts' not in req:
        req['_ts'] = _parse_ts(entry['startedDateTime'])

    if '_ts' not in resp:
        assert entry['time'] >= 0, req['url'] + " will be skipped because of negative 'time'"
        resp['_ts'] = req['_ts'] + entry['time'] / 1000

    req['headers'] = [x for x in req['headers'] if x['value'] != '[REDACTED]']
    resp['headers'] = [x for x in resp['headers'] if x['value'] != '[REDACTED]']

    return req, resp


def _parse_and_add_cookies_in_entry(entry):
    req_cookies = _get_cookies_from_headers(entry['request'], response=False)
    for cookie in req_cookies:
        if cookie not in entry['request']['cookies']:
            entry['request']['cookies'].append(cookie)

    resp_cookies = _get_cookies_from_headers(entry['response'], response=True)
    for cookie in resp_cookies:
        if cookie not in entry['response']['cookies']:
            entry['response']['cookies'].append(cookie)


def _get_cookies_from_headers(container, response=True):
    base = HTTPPart(container['headers'])
    headers_cookie_list = base.get_header_multi('cookie')
    for cookie in headers_cookie_list:
        yield _parse_cookie_value(cookie, response)


def _parse_cookie_value(cookie_value, response=True):
    result = {}
    cookie_parts = cookie_value.split(';')
    result['name'] = cookie_parts[0].split('=')[0]
    result['value'] = cookie_parts[0].split('=')[1]
    result['httpOnly'] = 'httponly' in (part.lower() for part in cookie_parts[1:])
    result['secure'] = 'secure' in (part.lower() for part in cookie_parts[1:])
    if not response:
        return result
    result['path'] = '/'
    result['expires'] = None
    keys_list = ['path', 'expires']
    for part in cookie_parts[1:]:
        for key in keys_list:
            if len(part.split(key + '=')) == 2:
                result[key] = part.split(key + '=')[1]
    return result


def _parse_ts(tstr):
    ts = dateutil.parser.parse(tstr)
    return ts.timestamp()


class HTTPPart:

    def __init__(self, headers=None) -> None:
        super().__init__()
        self.headers = [] if headers is None else headers
        self.ctype = ["", {}]
        self.ctype_guessed = ""
        self.ts = 0
        self.body = None
        self.raw_body = None

    def get_header_single(self, header):
        res = None
        for hdr in self.headers:
            if hdr['name'].lower() == header.lower():
                res = hdr['value']  # latter overrides earlier

        return res

    def get_header_multi(self, header):
        res = []
        for hdr in self.headers:
            if hdr['name'].lower() == header.lower():
                res.append(hdr['value'])

        return res