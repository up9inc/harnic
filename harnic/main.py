import argparse

from harnic.compare import har_compare
from harnic.har import HAR
from harnic.render import render_diff_to_json

my_parser = argparse.ArgumentParser()

my_parser.add_argument('from_file', action='store', type=str,
                       help='First traffic file')

my_parser.add_argument('to_file', action='store', type=str,
                       help='Second traffic file')

args = my_parser.parse_args()


print('Generating diffs...')
h1 = HAR(args.from_file)
h2 = HAR(args.to_file)
diff = har_compare(h1, h2)

render_diff_to_json((h1, h2), diff.records, diff.stats)
print('Comparison artifacts generated')
