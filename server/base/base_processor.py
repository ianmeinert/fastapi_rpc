# processor.py
import json
import os
from uuid import UUID

from marshmallow import ValidationError

from core.config import settings
from cxm.ccdschema import CcdSchema
from base.basemodel import Header, Response, ResponseBody, ResponseEncoder


class Processor:

    def __init__(self, txid: str, message: json):
        self.message = message
        self.header: json = message.get("header")
        self.body: json = message.get("body")
        self.txid = txid

    def validate_header(self):
        if "requestorId" not in self.header.keys():
            raise ValidationError(
                field_name="requestorId",
                message="header requestorId is missing"
            )

        if "methodName" not in self.header.keys():
            raise ValidationError(
                field_name="methodName",
                message="header methodName is missing",
            )

        if "txid" not in self.header.keys():
            self.header.setdefault("txid", self.txid)
        elif not self.header["txid"]:
            self.header["txid"] = self.txid
        else:
            try:
                UUID(self.header["txid"])
                # the uuid is valid and you can use it
                self.txid = self.header["txid"]
            except ValueError:
                print(('Client provided invalid transaction id: '
                       f'{self.header["txid"]}')
                      )
                print(f'Adjusted transaction id to: {self.txid}')
                self.header["txid"] = self.txid

    def load_schema(self):
        id = self.header.get("requestorId")
        methodName = self.header.get("methodName")
        print(self.header.get("txid"))
        loaded = None

        match id:
            case settings.ICD_ONE:
                match methodName:
                    case "ccd":
                        # validate the message"
                        loaded = CcdSchema().load(self.message)
                    case other:
                        raise ValidationError(
                            field_name="methodName",
                            message=f"methodName '{other}' is invalid",
                        )
            case other:
                raise ValidationError(
                    field_name="requestorId",
                    message=f"requestorId '{other}' is invalid",
                )

        return loaded

    def get_response(self, msgstatus="", errormsg=""):
        header = Header(
            requestorId=self.header.get("requestorId"),
            methodName=self.header.get("methodName"),
            txid=self.txid,
        )

        body = ResponseBody(msgstatus=msgstatus, errormsg=errormsg)
        response = Response(header, body)

        return json.dumps(response, indent=4, cls=ResponseEncoder)

    def get_error_response(self, error):
        ex_name = type(error).__name__

        msgstatus = ""
        errormsg = ""

        if ex_name == "KeyError":
            msgstatus = "MALFORMED HEADER"
            errormsg = f"'{error.args[0]}' is missing"
        elif ex_name == "ValidationError":
            msgstatus = "ERROR"
            errormsg = str(error.messages)

        return self.get_response(msgstatus, errormsg)

    def forward_request(self, obj, dir_name):
        # make sure the directory exists
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # encode Object into JSON formatted Data
        jsonData = json.dumps(obj, cls=ResponseEncoder)

        # decode JSON formatted Data
        msg = json.loads(jsonData)

        # store the body in a data frame
        body = msg.get("body")
        print(f"Message body {body}")

        # build the file path
        header = msg.get("header")
        base_filename = (
            f"{header.get('requestorId')}_"
            f"{header.get('methodName')}_"
            f"{self.txid}"
        )
        suffix = ".json"
        file_path = os.path.join(dir_name, base_filename + suffix)

        # save the file
        with open(file_path, "w") as fp:
            json.dump(body, fp, indent=4)
