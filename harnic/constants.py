SOFT_HEADER_KEYS = {'set-cookie', 'last-modified', 'expires'}
REGULAR_HEADERS = {
    'a-im',
    'accept', 'accept-charset', 'accept-datetime', 'accept-encoding', 'accept-language',
    'access-control-allow-credentials', 'access-control-allow-origin', 'access-control-request-headers',
    'access-control-request-method',
    'authorization', 'cache-control', 'connection', 'content-encoding', 'content-length', 'content-type', 'cookie',
    'date', 'dnt', 'expect', 'forwarded', 'from', 'front-end-https', 'host', 'http2-settings',
    'if-match', 'if-modified-since', 'if-none-match', 'if-range', 'if-unmodified-since',
    'max-forwards', 'origin', 'pragma', 'proxy-authorization', 'proxy-connection', 'range', 'referer',
    'save-data', 'sec-fetch-user', 'te', 'trailer', 'transfer-encoding', 'upgrade', 'upgrade-insecure-requests',
    'user-agent', 'via', 'warning',
    'x-att-deviceid', 'x-correlation-id',
    'x-forwarded-for', 'x-forwarded-host', 'x-forwarded-port', 'x-forwarded-proto',
    'x-http-method-override', 'x-real-ip', 'x-request-id', 'x-request-start', 'x-requested-with', 'x-uidh',
    'x-wap-profile',
    'x-envoy-expected-rq-timeout-ms', 'x-envoy-external-address',
    ':method', ':scheme', ':authority', ':path'
}
STRICT_REGULAR_HEADERS = {
    'accept', 'content-type',
}
SOFT_HEADER_KEYS.update(REGULAR_HEADERS - STRICT_REGULAR_HEADERS)

CONTENT_MEDIA_TYPES_SPECIAL = (
    'application/pdf',
    'application/font-woff2',
    'application/font-woff',
    'application/x-font-woff',
    'application/vnd.apple.mpegurl',
    'application/x-mpegurl',

)
CONTENT_LONG_SKIP_TYPES = ('text/css', 'text/javascript', 'application/javascript', 'text/html')
# MAX_BODY_SIZE = 50000
MAX_BODY_SIZE = 1000000

JSON_CTYPES = ('application/json', 'application/x-amz-json-1.1', 'application/reports+json')

JSON_INDENT = 2

PARTIAL_MATCH_CUTOFF = 0.5
FANCY_REPLACE_THRESHOLD_LEN = 256

# TODO: add assert that sum is 1
SCORE_COEFS = {
    'request': {
        'bodySize': 0.05,
        'query_params': 0.25,
        'headers': 0.2,
        'postData': 0.5,
    },
    'response': {
        'status': 0.25,
        'headers': 0.3,
        'content': 0.45,
    }
}

SCORE_HTTP_TX_TYPE_COEFS = {
    'request': 0.4,
    'response': 0.6,
}
