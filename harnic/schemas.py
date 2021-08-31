from marshmallow import Schema, fields, pre_dump

from harnic.compare.har import PermTag
from harnic.constants import CONTENT_LONG_SKIP_TYPES


class HarSchema(Schema):
    path = fields.Str()
    num_entries = fields.Method("get_num_entries")
    size = fields.Integer()

    def get_num_entries(self, object):
        return len(object.entries)


class UrlSchema(Schema):
    url = fields.Url()
    clean_url = fields.Url()
    query_params = fields.Dict()


class EntrySchema(Schema):
    metadata = fields.Mapping()
    request = fields.Nested('RequestSchema')
    response = fields.Nested('ResponseSchema')


class MessageSchema(Schema):
    _ts = fields.Float()
    cookies = fields.List(fields.Dict())
    headers = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))
    headers_size = fields.Integer()
    bodySize = fields.Integer()
    comment = fields.String()


class RequestSchema(MessageSchema):
    method = fields.String()
    url = fields.Nested('UrlSchema')
    http_version = fields.String()
    query_string = fields.List(fields.Dict())
    post_data = fields.Raw()


class ResponseSchema(MessageSchema):
    status = fields.Integer()
    status_text = fields.String()
    http_version = fields.String()
    content = fields.Raw()
    redirect_url = fields.Url()

    @pre_dump
    def clear_content(self, in_data, **kwargs):
        content = in_data['content']
        if content['size'] > 2500 and any(skip_type in content['mimeType'] for skip_type in CONTENT_LONG_SKIP_TYPES):
            in_data['content']['text'] = None
        return in_data


class StatsSchema(Schema):
    equal = fields.Method("get_equal")
    diff = fields.Method("get_diff")
    insert = fields.Method("get_insert")
    delete = fields.Method("get_delete")
    ratio = fields.Float()

    def get_equal(self, object):
        return object[PermTag.EQUAL]

    def get_diff(self, object):
        return object[PermTag.DIFF]

    def get_insert(self, object):
        return object[PermTag.INSERT]

    def get_delete(self, object):
        return object[PermTag.DELETE]
