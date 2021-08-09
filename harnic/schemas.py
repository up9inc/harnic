from marshmallow import Schema, fields, pre_dump

from harnic.constants import CONTENT_LONG_SKIP_TYPES, CONTENT_SKIP_TYPES


class UrlSchema(Schema):
    url = fields.Url()
    clean_url = fields.Url()
    query_params = fields.Dict()


class EntrySchema(Schema):
    metadata = fields.Mapping()
    request = fields.Nested('RequestSchema')
    response = fields.Nested('ResponseSchema')


class MessageSchema(Schema):
    cookies = fields.List(fields.Dict())
    headers = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))
    headers_size = fields.Integer()
    body_size = fields.Integer()
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
            in_data['content']['text'] = "Data is too big to display"
        elif any(skip_type in content['mimeType'] for skip_type in CONTENT_SKIP_TYPES):
            in_data['content']['text'] = f"Raw '{content['mimeType']}' data not displayed"
        return in_data
