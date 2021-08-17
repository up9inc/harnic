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

# lol
with open('harnic-spa/build/data.js', 'w+') as file_js, open('harnic-spa/build/data.json') as file_json:
    file_js.write('window.globalData = ')
    file_js.writelines(l for l in file_json)
    file_js.write(';')
print('Comparison artifacts generated')
