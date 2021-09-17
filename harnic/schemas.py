from marshmallow import Schema, fields, pre_dump

from harnic.compare.matcher import PermTag


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
    post_data = fields.Method("get_post_data")

    def get_post_data(self, object):
        return object.get('postData')


class ResponseSchema(MessageSchema):
    status = fields.Integer()
    status_text = fields.String()
    http_version = fields.String()
    content = fields.Raw()
    redirect_url = fields.Url()

    @pre_dump
    def clear_content(self, in_data, **kwargs):
        return in_data
        # content = in_data['content']
        # if content['size'] > 2500 and any(skip_type in content['mimeType'] for skip_type in CONTENT_LONG_SKIP_TYPES):
        #     in_data['content']['text'] = None
        # return in_data


class StatsSchema(Schema):
    matched = fields.Method("get_matched")
    modified = fields.Method("get_modified")
    added = fields.Method("get_added")
    removed = fields.Method("get_removed")
    ratio = fields.Float()

    def get_matched(self, object):
        return object[PermTag.EQUAL]

    def get_modified(self, object):
        return object[PermTag.DIFF]

    def get_added(self, object):
        return object[PermTag.INSERT]

    def get_removed(self, object):
        return object[PermTag.DELETE]
