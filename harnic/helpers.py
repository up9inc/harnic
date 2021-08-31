import textwrap

from tabulate import tabulate

from harnic.compare.matcher import PermTag
from harnic.compare.schemas import DiffKpisSchema
from harnic.render import render_diff_to_json


def generate_artifacts(diff, out_dir):
    diffjson = render_diff_to_json(diff)

    with open(out_dir + '/data.js', 'w+') as file_js:
        file_js.write('window.globalData = ')
        file_js.write(diffjson)
        file_js.write(';')

    with open(out_dir + '/kpis.json', 'w+') as kpis_file:
        kpis_file.write(DiffKpisSchema().dumps(diff, indent=2))


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
        ('Match ratio',
         get_match_ratio(stats['with_reorders']['ratio']),
         get_match_ratio(stats['strict_order']['ratio'])),
    ]
    table.extend(  # _ == k1
        (rename_key_table[k], v1, v2)
        for (k, v1), (_, v2) in zip(stats['with_reorders'].items(), stats['strict_order'].items())
        if k in rename_key_table.keys()
    )
    headers = ["", "With Reorders", "Strict Order"]
    return tabulate(table, headers=headers, tablefmt='github')


def stats_report(diff):
    return textwrap.dedent(f"""

        Comparison stats:
        {diff.file1.pretty_repr()}
        {diff.file2.pretty_repr()}

    """) + format_diff_stats(diff.stats)
