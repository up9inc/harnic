from functools import partial

from harnic.compare.utils import dict_compare, scalars_compare, content_compare
from harnic.constants import SOFT_HEADER_KEYS

headers_compare = partial(dict_compare, exceptions=SOFT_HEADER_KEYS, exculde_values=True)


# TODO: may this be a func?
class EntryDiff:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.equal = None
        self.comparisons = self._get_diff()

    def _get_diff(self):
        # method and url are not handled here as long as they are part of the entry hash
        comparisons = {'request': {}, 'response': {}}

        comparisons['request']['bodySize'] = scalars_compare(self.a.request['bodySize'],
                                                             self.b.request['bodySize'])
        comparisons['request']['query_params'] = dict_compare(self.a.request['url'].query_params,
                                                              self.b.request['url'].query_params)
        comparisons['request']['headers'] = headers_compare(self.a.request['headers'],
                                                            self.b.request['headers'])

        comparisons['response']['status'] = scalars_compare(self.a.response['status'],
                                                            self.b.response['status'])
        comparisons['response']['headers'] = headers_compare(self.a.response['headers'],
                                                             self.b.response['headers'])
        comparisons['response']['content'] = content_compare(self.a.response['content'],
                                                             self.b.response['content'])

        self.equal = all(all(cmp.equal for cmp in criteria.values()) for criteria in comparisons.values())
        return comparisons
