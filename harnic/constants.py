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

CONTENT_SKIP_TYPES = ('image/png', 'image/jpg', 'image/jpeg', 'image/gif')
CONTENT_LONG_SKIP_TYPES = ('text/css', 'text/javascript', 'application/javascript', 'text/html')

JSON_INDENT = 2
