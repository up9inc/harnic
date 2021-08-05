from collections import defaultdict, namedtuple
from functools import partial

Comparison = namedtuple('Comparison', ['equal', 'strict_equal', 'diff'])
DictDiff = namedtuple('DictDiff', ['added', 'removed', 'modified', 'same'], defaults=[set(), set(), dict(), set()])


def headers_list_to_map(headers):
    result = defaultdict(list)
    for header in headers:
        name, value = header['name'], header['value']
        result[name].append(value)
    for value in result.values():
        value.sort()
    return result


def dict_compare(d1, d2, exceptions=()):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {key: (d1[key], d2[key]) for key in shared_keys if d1[key] != d2[key]}  # TODO: depends on keys order
    same = set(key for key in shared_keys if d1[key] == d2[key])  # TODO: same
    equal = {k: v for k, v in d1.items() if k not in exceptions} == \
            {k: v for k, v in d2.items() if k not in exceptions}
    return Comparison(equal, d1 == d2, DictDiff(added, removed, modified, same))


headers_compare = partial(dict_compare, exceptions=('Cookie',))
