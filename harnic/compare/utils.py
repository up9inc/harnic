from collections import namedtuple

Comparison = namedtuple('Comparison', ['equal', 'strict_equal', 'diff'])
DictDiff = namedtuple('DictDiff', ['added', 'removed', 'modified', 'same'], defaults=[set(), set(), dict(), set()])


def dict_compare(d1, d2, exceptions=()):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d2_keys.intersection(d1_keys)
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    modified = {key: (d1[key], d2[key]) for key in shared_keys if d1[key] != d2[key]}  # TODO: depends on keys order
    same = set(key for key in shared_keys if d1[key] == d2[key])  # TODO: same
    equal = {k: v for k, v in d1.items() if k not in exceptions} == \
            {k: v for k, v in d2.items() if k not in exceptions}
    return Comparison(equal, d1 == d2, DictDiff(added, removed, modified, same))


def scalars_compare(s1, s2):
    equal = strict_equal = s1 == s2
    return Comparison(equal, strict_equal, None)
