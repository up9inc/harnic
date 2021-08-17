import json
import time

from jinja2 import Environment, FileSystemLoader, select_autoescape

from compare import har_compare
from har import HAR
from harnic.compare import DiffRecordSchema
from harnic.schemas import StatsSchema


def timectime(s):
    return time.ctime(s)  # datetime.datetime.fromtimestamp(s)


env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
env.filters['ctime'] = timectime


def render_diff(hars, records, output_name='index.html'):
    template = env.get_template("index.html")
    context = {
        'hars': hars,
        'records': records,
    }
    template.stream(**context).dump(output_name)


def render_diff_to_json(hars, records, stats):
    result = {
        'hars': [hars[0].path, hars[1].path],
        'records': DiffRecordSchema().dump(records, many=True),
        'stats': StatsSchema().dump(stats)
    }
    with open('harnic-spa/public/data.json', 'w+') as file:
        json.dump(result, file)


if __name__ == '__main__':
    h1 = HAR('hars/e-maxx.ru/1.har')
    h2 = HAR('hars/e-maxx.ru/2.har')
    diff = har_compare(h1, h2)

    # render_diff((h1, h2), diff.records)
    render_diff_to_json((h1, h2), diff.records, diff.stats)

    with open('harnic-spa/build/data.js', 'w+') as file_js, open('harnic-spa/build/data.json') as file_json:
        file_js.write('window.globalData = ')
        file_js.writelines(l for l in file_json)
        file_js.write(';')