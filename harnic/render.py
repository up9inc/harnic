import json
import os

from harnic.compare import DiffRecordSchema, har_compare
from harnic.har import HAR
from harnic.schemas import StatsSchema


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

    with open(os.path.dirname(__file__) + '/../harnic-spa/public/data.json', 'w+') as file:
        result = render_diff_to_json((h1, h2), diff.records, diff.stats)
        file.write(result)

    with open(os.path.dirname(__file__) + '/../harnic-spa/public/data.js', 'w+') as file_js, open(
            os.path.dirname(__file__) + '/../harnic-spa/public/data.json') as file_json:
        file_js.write('window.globalData = ')
        file_js.writelines(l for l in file_json)
        file_js.write(';')
