from collections import namedtuple, defaultdict

Comparison = namedtuple('Comparison', ['equal', 'diff'])
DictDiff = namedtuple('DictDiff', ['added', 'removed', 'modified', 'same'], defaults=[set(), set(), set(), dict()])


def dict_compare(d1, d2):
    if d1 == d2:
        return Comparison(True, DictDiff())
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {key: (d1[key], d2[key]) for key in shared_keys if d1[key] != d2[key]}  # TODO: depends on keys order
    same = set(key for key in shared_keys if d1[key] == d2[key])  # TODO: same
    return Comparison(False, DictDiff(added, removed, modified, same))


def headers_list_to_map(headers):
    result = defaultdict(list)
    for header in headers:
        name, value = header['name'], header['value']
        result[name].append(value)
    for value in result.values():
        value.sort()
    return result
