import os
from collections import defaultdict

from tabulate import tabulate

from harnic.compare.har import PermTag
from harnic.constants import CONTENT_MEDIA_TYPES_SPECIAL

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


def format_diff_stats(stats):
    def get_match_ratio(ratio):
        return "{:.2f}%".format(ratio * 100)

    rename_key_table = {
        PermTag.EQUAL: 'Matched',
        PermTag.DIFF: 'Modified',
        PermTag.INSERT: 'Added',
        PermTag.DELETE: 'Removed',
    }
    table = [
        ('Match ratio', get_match_ratio(stats['original']['ratio']), get_match_ratio(stats['with_reorders']['ratio'])),
    ]
    table.extend(  # _ == k1
        (rename_key_table[k], v1, v2)
        for (k, v1), (_, v2) in zip(stats['original'].items(), stats['with_reorders'].items())
        if k in rename_key_table.keys()
    )
    headers = ["", "Original", "With Reorders"]
    return tabulate(table, headers=headers, tablefmt='github')
