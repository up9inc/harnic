from functools import partial

from harnic.compare.utils import dict_compare

headers_compare = partial(dict_compare, exceptions=('Cookie',))


# TODO: this may be a func?
class EntryDiff:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.equal = None
        self.fields = self._get_diff()

    def _get_diff(self):
        # method and url are not handled here as long as they are part of the entry hash
        fields = {'request': {}, 'response': {}}

        qs_cmp = dict_compare(self.a.request['url'].query_params,
                              self.b.request['url'].query_params)
        headers_cmp = headers_compare(self.a.request['headers'],
                                      self.b.request['headers'])
        fields['request']['query_params'] = qs_cmp
        fields['request']['headers'] = headers_cmp

        self.equal = all(c.equal for c in [qs_cmp, headers_cmp])
        return fields
