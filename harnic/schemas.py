from marshmallow import Schema, fields


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
