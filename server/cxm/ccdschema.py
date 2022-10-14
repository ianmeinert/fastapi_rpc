from marshmallow import Schema, ValidationError, fields, post_load
from core.config import settings
from cxm.ccdmodel import Body, Ccd, Document, Header


class HeaderSchema(Schema):
    # make sure the contract ID is legit
    def validate_contract_id(value):
        if not value or value != settings.ICD_ONE:
            raise ValidationError(message="Valid id required")

    # make sure the contract is only requesting approved data
    def validate_methodName(value):
        if not value or value not in settings.METHODS_ONE:
            raise ValidationError(message="Authorized query type required")

    requestorId = fields.Str(required=False, validate=validate_contract_id)
    methodName = fields.Str(required=False, validate=validate_methodName)
    txid = fields.Str()

    @post_load
    def make_header(self, data, **kwargs):
        return Header(**data)


class DocumentSchema(Schema):

    # make sure the contract is only requesting approved data
    def validate_string_is_not_missing(value):
        if not value:
            raise ValidationError(message="Missing field value is required")

    docid = fields.Str(
        required=True,
        validate=validate_string_is_not_missing
        )

    filenum = fields.Str(
        required=True,
        validate=validate_string_is_not_missing
        )

    status = fields.Str(
        required=True,
        validate=validate_string_is_not_missing
        )

    program = fields.Str(
        required=True,
        validate=validate_string_is_not_missing
        )

    completeddate = fields.Str(
        required=True,
        validate=validate_string_is_not_missing
        )

    @post_load
    def make_claim(self, data, **kwargs):
        return Document(**data)


class BodySchema(Schema):
    documents = fields.Nested(DocumentSchema, many=True)

    @post_load
    def make_body(self, data, **kwargs):
        return Body(**data)


class CcdSchema(Schema):
    header = fields.Nested(HeaderSchema)
    body = fields.Nested(BodySchema)

    @post_load
    def make_ccd(self, data, **kwargs):
        return Ccd(**data)
