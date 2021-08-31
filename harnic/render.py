import json
import os

from harnic.compare import har_compare
from harnic.compare.har import create_compact_records_index
from harnic.compare.schemas import DiffCompactSchema, DiffKpisSchema
from harnic.har import HAR


def render_diff_to_json(diff, format='compact'):
    result = {}
    if format == 'compact':
        compact_index = create_compact_records_index(diff)
        result['diff'] = DiffCompactSchema().dump(compact_index)
    else:
        raise NotImplementedError()
    result['kpis'] = DiffKpisSchema().dump(diff)

    return json.dumps(result)


if __name__ == '__main__':
    h1 = HAR('hars/e-maxx.ru/1.har')
    h2 = HAR('hars/e-maxx.ru/2.har')
    # h1 = HAR('hars/big/1.har')
    # h2 = HAR('hars/big/2.har')
    diff = har_compare(h1, h2)

    with open(os.path.dirname(__file__) + '/../harnic-spa/public/data.json', 'w+') as file:
        result = render_diff_to_json(diff)
        file.write(result)

    with open(os.path.dirname(__file__) + '/../harnic-spa/public/data.js', 'w+') as file_js, open(
            os.path.dirname(__file__) + '/../harnic-spa/public/data.json') as file_json:
        file_js.write('window.globalData = ')
        file_js.writelines(l for l in file_json)
        file_js.write(';')
