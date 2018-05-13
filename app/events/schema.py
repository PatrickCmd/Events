from marshmallow import Schema
from webargs import fields, validate


class CategorySchema(Schema):
    id = fields.Int(dump_only=True) # read-only (won't be parsed by webargs)
    # required field
    name =  fields.Str(required=True, validate=validate.Length(3))
    created_by = fields.Int(dump_only=True)

    class Meta:
        strict = True


class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    owner = fields.Int(dump_only=True)
    category_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(3))
    description = fields.Str(missing='')
    price = fields.Int(missing=0)
    location = fields.Str(required=True, validate=validate.Length(3))
    type = fields.Str(required=True, validate=validate.Length(3))
    maxNumOfAttendees = fields.Int(required=True)
    dueDate = fields.DateTime(dump_only=True)
    dateCreated = fields.DateTime(dump_only=True)
    dateModified = fields.DateTime(dump_only=True)
    isPublic = fields.Bool(dump_only=True)

    class Meta:
        strict = True

