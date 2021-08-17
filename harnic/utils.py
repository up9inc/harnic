import os
from collections import defaultdict

SPA_BASE = os.getenv('SPA_LOCATION', 'harnic-spa')


def headers_list_to_map(headers):
    result = defaultdict(list)
    for header in headers:
        name, value = header['name'], header['value']
        result[name.lower()].append(value)
    for value in result.values():
        value.sort()
    return result
