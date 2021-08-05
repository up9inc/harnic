from collections import defaultdict


def headers_list_to_map(headers):
    result = defaultdict(list)
    for header in headers:
        name, value = header['name'], header['value']
        result[name].append(value)
    for value in result.values():
        value.sort()
    return result
