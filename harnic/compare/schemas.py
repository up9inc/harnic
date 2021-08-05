from marshmallow import Schema, fields

from harnic.schemas import EntrySchema


class DictDiffSchema(Schema):
    added = fields.List(fields.String())
    modified = fields.Dict()
    removed = fields.List(fields.String())
    same = fields.List(fields.String())


class ComparisonSchema(Schema):
    equal = fields.Bool()
    strict_equal = fields.Bool()
    diff = fields.Nested('DictDiffSchema')


class EntryDiffSchema(Schema):
    equal = fields.Bool()
    comparisons = fields.Dict(values=fields.Dict(values=fields.Nested('ComparisonSchema')))


class PairSchema(Schema):
    a = fields.Nested(EntrySchema)
    b = fields.Nested(EntrySchema)


class DiffRecordSchema(Schema):
    pair = fields.Nested('PairSchema')
    diff = fields.Nested('EntryDiffSchema')
    tag = fields.String()
