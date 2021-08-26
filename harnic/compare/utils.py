from collections import namedtuple
from difflib import _mdiff

from harnic.constants import CONTENT_LONG_SKIP_TYPES, CONTENT_SKIP_TYPES

Comparison = namedtuple('Comparison', ['equal', 'strict_equal', 'diff'])
DictDiff = namedtuple('DictDiff', ['added', 'removed', 'modified', 'same'], defaults=[set(), set(), dict(), set()])


def split_diff(fromlines, tolines, **kwargs):
    diffs = _mdiff(fromlines, tolines, **kwargs)

    # Collects mdiff output into separate lists
    fromlist, tolist, flaglist = [], [], []
    # pull from/to data and flags from mdiff style iterator
    for fromdata, todata, flag in diffs:
        fromlist.append(fromdata[1])
        tolist.append(todata[1])
        flaglist.append(flag)
    return fromlist, tolist, flaglist


def dict_compare(d1, d2, exceptions=(), exculde_values=False):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d2_keys.intersection(d1_keys)
    added = d2_keys - d1_keys
    removed = d1_keys - d2_keys
    modified = {
        key: (d1[key], d2[key], True if exculde_values else key in exceptions)
        for key in shared_keys
        if d1[key] != d2[key]
    }  # TODO: depends on keys order
    same = set(key for key in shared_keys if d1[key] == d2[key])  # TODO: same
    if exculde_values:
        equal = d1.keys() == d2.keys()
    else:
        equal = {k: v for k, v in d1.items() if k not in exceptions} == \
                {k: v for k, v in d2.items() if k not in exceptions}
    return Comparison(equal, d1 == d2, DictDiff(added, removed, modified, same))


def scalars_compare(s1, s2):
    equal = strict_equal = s1 == s2
    return Comparison(equal, strict_equal, None)


def content_compare(c1, c2):
    # All content keys except 'text' are soft
    keys = set(c1.keys()).union(set(c2.keys()))
    keys.discard('text')
    cmp = dict_compare(c1, c2, exceptions=keys)

    # TODO: bad
    for c in (c1, c2):
        if c['size'] > 2500 and any(skip_type in c['mimeType'] for skip_type in CONTENT_LONG_SKIP_TYPES):
            return cmp._replace(diff=cmp.diff._replace(modified={**cmp.diff.modified, 'text': None}))
        elif any(skip_type in c['mimeType'] for skip_type in CONTENT_SKIP_TYPES):
            return cmp._replace(diff=cmp.diff._replace(modified={**cmp.diff.modified, 'text': None}))

    if 'text' in cmp.diff.modified.keys():
        try:
            diff = split_diff(c1['text'].splitlines(), c2['text'].splitlines())
        except KeyError:
            pass
        else:
            return cmp._replace(diff=cmp.diff._replace(modified={**cmp.diff.modified, 'text': diff}))
    return cmp
