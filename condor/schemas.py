from marshmallow import Schema
from marshmallow import fields


class RecordSchema(Schema):
    uuid = fields.Str()
    title = fields.Str()
    abstract = fields.Str()
    keywords = fields.List(fields.Str)
    raw = fields.Raw()


class ModelSchema(Schema):
    words = fields.List(fields.Str)
    model_path = fields.Str()
    created_at = fields.DateTime()
