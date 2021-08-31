import os
from collections import defaultdict

from harnic.constants import CONTENT_MEDIA_TYPES_SPECIAL, JSON_CTYPES

SPA_BASE = os.getenv('SPA_LOCATION', 'harnic-spa')


def headers_list_to_map(headers):
    result = defaultdict(list)
    for header in headers:
        name, value = header['name'], header['value']
        result[name.lower()].append(value)
    for value in result.values():
        value.sort()
    return result


def is_ctype_ignored(ctype):
    ctype = ctype and ctype.split(';')[0].strip()
    if ctype in (
            "application/javascript", "application/x-javascript", 'text/css', 'application/font-woff2',
            'application/font-woff', 'application/x-font-woff', 'application/pdf') \
            or (ctype and ctype.startswith("image/")) \
            or (ctype and ctype.startswith("font/")) \
            or (ctype and ctype.startswith("video/")) \
            or (ctype and ctype.startswith("text/javascript")):
        return True

    return False


def is_ctype_media(ctype):
    ctype = ctype and ctype.split(';')[0].strip()
    if not ctype:
        return False
    if ctype.startswith('image/') or \
            ctype.startswith('font/') or \
            ctype.startswith('video/') or \
            ctype in CONTENT_MEDIA_TYPES_SPECIAL:
        return True
    return False


def is_ctype_json(ctype):
    ctype = ctype and ctype.split(';')[0].strip()
    if not ctype:
        return False
    if ctype in JSON_CTYPES:
        return True
    return False


def sizeof_fmt(num, suffix='b'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
