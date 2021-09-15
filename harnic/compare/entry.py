from functools import partial

from harnic.compare.utils import content_compare, dict_compare, dict_product, qp_compare, scalars_compare
from harnic.constants import SCORE_COEFS, SCORE_HTTP_TX_TYPE_COEFS, SOFT_HEADER_KEYS

headers_compare = partial(dict_compare, exceptions=SOFT_HEADER_KEYS, exculde_values=True)


# TODO: may this be a func?
class EntryDiff:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.equal = None
        self.score = {}
        self.comparisons = self._get_diff()

    def _get_diff(self):
        # method and url are not handled here as long as they are part of the entry hash
        comparisons = {'request': {}, 'response': {}}

        diff_score = {
            'request': {},
            'response': {},
        }

        cmp = scalars_compare(self.a.request['url'].clean_url, self.b.request['url'].clean_url)
        diff_score['request']['url'] = cmp.score

        cmp = scalars_compare(self.a.request['bodySize'], self.b.request['bodySize'])
        comparisons['request']['bodySize'] = cmp

        cmp = qp_compare(self.a.request['url'].query_params, self.b.request['url'].query_params)
        comparisons['request']['query_params'], diff_score['request']['query_params'] = cmp, cmp.score

        cmp = headers_compare(self.a.request['headers'], self.b.request['headers'])
        comparisons['request']['headers'], diff_score['request']['headers'] = cmp, cmp.score

        # TODO: implement postData cmp
        diff_score['request']['postData'] = 1  # Treat same for now

        cmp = scalars_compare(self.a.response['status'], self.b.response['status'])
        comparisons['response']['status'], diff_score['response']['status'] = cmp, cmp.score

        cmp = headers_compare(self.a.response['headers'], self.b.response['headers'])
        comparisons['response']['headers'], diff_score['response']['headers'] = cmp, cmp.score

        cmp = content_compare(self.a.response, self.b.response)
        comparisons['response']['content'], diff_score['response']['content'] = cmp, cmp.score

        self.equal = all(all(cmp.equal for cmp in criteria.values()) for criteria in comparisons.values())

        self.score['full'] = diff_score
        diff_score_with_coefs = {
            'request': sum(dict_product(diff_score['request'], SCORE_COEFS['request']).values()),
            'response': sum(dict_product(diff_score['response'], SCORE_COEFS['response']).values()),
        }
        self.score['by_http_tx_type'] = diff_score_with_coefs
        diff_score_with_coefs = dict_product(diff_score_with_coefs, SCORE_HTTP_TX_TYPE_COEFS)
        final_score = sum(diff_score_with_coefs.values())
        self.score['final'] = final_score

        return comparisons
