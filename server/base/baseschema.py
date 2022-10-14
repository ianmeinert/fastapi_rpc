from marshmallow import Schema, fields


class HeaderSchema(Schema):
    requestorId = fields.Str(
        required=True, error_messages={
            "required": {"message": "Contract ID required"}
            }
    )
    methodName = fields.Str(
        required=True, error_messages={
            "required": {"message": "Request type required"}
            }
    )
    txid = fields.Str()


class BodySchema(Schema):
    msgstatus = fields.Str(
        required=True,
        error_messages={
            "required": {"message": "Status not provided"}
            }
    )

    errormsg = fields.Str()


class ResponseSchema(Schema):
    header = HeaderSchema()
    body = BodySchema()
