

from marshmallow import Schema, fields, INCLUDE, ValidationError


class TodoSchema(Schema):
    id = fields.Int(dump_only = True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)