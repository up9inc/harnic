from difflib import _mdiff

import textdistance


class Comparison:
    def __init__(self, equal, strict_equal, diff, score):
        self.equal = equal
        self.strict_equal = strict_equal
        self.diff = diff
        self.score = score


class DictDiff:
    def __init__(self, added=None, removed=None, modified=None, same=None):
        self.added = added if added is not None else set()
        self.removed = removed if removed is not None else set()
        self.modified = modified if modified is not None else set()
        self.same = same if same is not None else set()


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


def dict_product(d1, d2):
    return {key: d1.get(key, 0) * d2[key] for key in d2.keys()}


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

    try:
        total_soft_diffs = len([v for v in modified.values() if v[2]])
        score = 2.0 * (len(same) + total_soft_diffs) / (len(d1_keys) + len(d2_keys))
    except ZeroDivisionError:
        score = 1
    return Comparison(equal, d1 == d2, DictDiff(added, removed, modified, same), score)


def scalars_compare(s1, s2):
    equal = strict_equal = s1 == s2
    return Comparison(equal, strict_equal, None, int(equal))


def qp_compare(qp1, qp2):
    # All query params are soft
    keys = set(qp1.keys()).union(set(qp2.keys()))
    cmp = dict_compare(qp1, qp2, exceptions=keys)
    return cmp


def text_compare(t1, t2):
    t1, t2 = str(t1), str(t2)
    splited1, splited2 = t1.splitlines(), t2.splitlines()
    # We compare strings as strings (not lists) if text is a single string
    if len(splited1) == 1 and len(splited2) == 1:
        cmp1, cmp2 = t1, t2
    else:
        cmp1, cmp2 = splited1, splited2
    return textdistance.levenshtein.normalized_similarity(cmp1, cmp2)


def content_compare(r1, r2):
    c1, raw1 = r1['content'], r1.get('raw_body')
    c2, raw2 = r2['content'], r2.get('raw_body')
    # All content keys except 'text' are soft
    keys = set(c1.keys()).union(set(c2.keys()))
    keys.discard('text')
    cmp = dict_compare(c1, c2, exceptions=keys)

    text_modified = cmp.diff.modified.get('text', ())
    cmp.score = 1
    if text_modified and None not in text_modified:
        try:
            diff = split_diff(c1['text'].splitlines(), c2['text'].splitlines())
        except KeyError:
            pass
        else:
            cmp.score = text_compare(c1['text'], c2['text'])
            cmp.diff.modified['text'] = diff
    else:
        # We should check for raw equality in case cleaned failed
        if raw1 != raw2:
            cmp.score = text_compare(c1['text'], c2['text'])
            # Values are skipped anyway so we just mark a diff without inner explanation
            cmp.diff.modified['text'] = None

    return cmp
