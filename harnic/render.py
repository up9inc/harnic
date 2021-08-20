import json
import os

from harnic.compare import har_compare
from harnic.compare.har import create_compact_records_index
from harnic.compare.schemas import DiffCompactSchema
from harnic.har import HAR


def render_diff_to_json(hars, diff, format='compact'):
    result = {
        'hars': [hars[0].path, hars[1].path],
    }

    if format == 'compact':
        compact_index = create_compact_records_index(diff)
        result['diff'] = DiffCompactSchema().dump(compact_index)
    else:
        raise NotImplementedError()

    return json.dumps(result)


if __name__ == '__main__':
    h1 = HAR('hars/e-maxx.ru/1.har')
    h2 = HAR('hars/e-maxx.ru/2.har')
    diff = har_compare(h1, h2)

    with open(os.path.dirname(__file__) + '/../harnic-spa/public/data1 .json', 'w+') as file:
        result = render_diff_to_json((h1, h2), diff)
        file.write(result)

    with open(os.path.dirname(__file__) + '/../harnic-spa/public/data1 .js', 'w+') as file_js, open(
            os.path.dirname(__file__) + '/../harnic-spa/public/data1 .json') as file_json:
        file_js.write('window.globalData = ')
        file_js.writelines(l for l in file_json)
        file_js.write(';')
