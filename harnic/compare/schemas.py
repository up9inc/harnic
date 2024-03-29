from marshmallow import Schema, fields

from harnic.schemas import EntrySchema, StatsSchema, HarSchema


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
    score = fields.Dict()


class PairSchema(Schema):
    a = fields.Nested(EntrySchema)
    b = fields.Nested(EntrySchema)


class DiffRecordSchema(Schema):
    pair = fields.Nested('PairSchema')
    diff = fields.Nested('EntryDiffSchema')
    tag = fields.Method('get_diff_tag')
    is_reordering = fields.Method('get_is_reordering')

    def get_diff_tag(self, object):
        return object.tag.value

    def get_is_reordering(self, object):
        if object.reordering:
            return True
        return False


class DiffCompactSchema(Schema):
    index = fields.Dict(keys=fields.UUID(), values=fields.Nested('DiffRecordSchema'))
    strict_order_records = fields.List(fields.UUID())
    reordered_records = fields.List(fields.UUID())


class DiffStatsSchema(Schema):
    with_reorders = fields.Nested(StatsSchema)
    strict_order = fields.Nested(StatsSchema)


class DiffKpisSchema(Schema):
    file1 = fields.Nested(HarSchema)
    file2 = fields.Nested(HarSchema)
    stats = fields.Nested(DiffStatsSchema)
