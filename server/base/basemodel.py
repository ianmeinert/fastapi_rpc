from json import JSONEncoder
import uuid


class Header:
    def __init__(self, requestorId, methodName, txid):
        self.requestorId = requestorId
        self.methodName = methodName
        self.txid = uuid.uuid4().hex if not txid else txid

    def __repr__(self):
        return (
            f"<Header(requestorId={self.requestorId!r}, "
            f"methodName={self.methodName!r}, "
            f"txid={self.txid!r}>"
        )


class ResponseBody:
    def __init__(self, msgstatus, errormsg):
        self.msgstatus = msgstatus
        self.errormsg = errormsg

    def __repr__(self):
        return (
            f"<ResponseBody(msgstatus={self.msgstatus!r},"
            f"errormsg={self.errormsg!r}>"
        )


class Response:
    def __init__(self, header, body):
        self.header = header
        self.body = body

    def __repr__(self):
        return f"<Response(header={self.header!r}, body={self.body!r}>"


class ResponseEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
