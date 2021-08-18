import os
from collections import defaultdict

from tabulate import tabulate

from harnic.compare.har import PermTag

SPA_BASE = os.getenv('SPA_LOCATION', 'harnic-spa')


def headers_list_to_map(headers):
    result = defaultdict(list)
    for header in headers:
        name, value = header['name'], header['value']
        result[name.lower()].append(value)
    for value in result.values():
        value.sort()
    return result


def format_stats(stats):
    rename_key_table = {
        PermTag.EQUAL: 'Matched',
        PermTag.DIFF: 'Diffs',
        PermTag.INSERT: 'Added',
        PermTag.DELETE: 'Removed',

    }
    table = [('Match ratio', "{:.2f}%".format((1 - stats['ratio']) * 100))]
    table.extend((rename_key_table[k], v) for k, v in stats.items() if k in rename_key_table.keys())
    headers = ["Label", "Value"]
    return tabulate(table, headers=headers, tablefmt='github')
