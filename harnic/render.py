import json
import os
import time

from jinja2 import Environment, FileSystemLoader, select_autoescape

from harnic.compare import DiffRecordSchema, har_compare
from harnic.har import HAR
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

    return json.dumps(result)


if __name__ == '__main__':
    h1 = HAR('hars/e-maxx.ru/1.har')
    h2 = HAR('hars/e-maxx.ru/2.har')
    diff = har_compare(h1, h2)

    # render_diff((h1, h2), diff.records)
    with open('harnic-spa/public/data.json', 'w+') as file:
        result = render_diff_to_json((h1, h2), diff.records, diff.stats)
        json.dump(result, file)

    with open(os.path.dirname(__file__) + '/../../harnic-spa/build/data.js', 'w+') as file_js, open(
            os.path.dirname(__file__) + '/../../harnic-spa/public/data.json') as file_json:
        file_js.write('window.globalData = ')
        file_js.writelines(l for l in file_json)
        file_js.write(';')
