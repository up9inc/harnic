from functools import partial

from harnic.compare.utils import dict_compare, scalars_compare
from harnic.constants import HEADER_NOT_STRICT_KEYS, CONTENT_NOT_STRICT_KEYS

headers_compare = partial(dict_compare, exceptions=HEADER_NOT_STRICT_KEYS)
content_compare = partial(dict_compare, exceptions=CONTENT_NOT_STRICT_KEYS)


# TODO: may this be a func?
class EntryDiff:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.equal = None
        self.fields = self._get_diff()

    def _get_diff(self):
        # method and url are not handled here as long as they are part of the entry hash
        fields = {'request': {}, 'response': {}}

        fields['request']['bodySize'] = scalars_compare(self.a.request['bodySize'],
                                                        self.b.request['bodySize'])
        fields['request']['query_params'] = dict_compare(self.a.request['url'].query_params,
                                                         self.b.request['url'].query_params)
        fields['request']['headers'] = headers_compare(self.a.request['headers'],
                                                       self.b.request['headers'])

        fields['response']['status'] = scalars_compare(self.a.response['status'],
                                                       self.b.response['status'])
        fields['response']['headers'] = headers_compare(self.a.response['headers'],
                                                        self.b.response['headers'])
        fields['response']['content'] = content_compare(self.a.response['content'],
                                                        self.b.response['content'])

        self.equal = all(all(cmp.equal for cmp in criteria.values()) for criteria in fields.values())
        return fields
