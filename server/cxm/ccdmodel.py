class Document:
    def __init__(
        self,
        docid: str,
        filenum: str,
        status: str,
        program: str,
        completeddate: str,
    ):
        self.docid = docid
        self.filenum = filenum
        self.status = status
        self.program = program
        self.completeddate = completeddate

    def __repr__(self):
        return (
            f"<Document(docid={self.docid!r}, filenum={self.filenum!r}, "
            f"status={self.status!r}, program={self.program!r}, "
            f"completeddate={self.completeddate!r}>"
        )


class Header:
    def __init__(self, requestorId: str, methodName: str, txid: str):
        self.requestorId = requestorId
        self.methodName = methodName
        self.txid = txid

    def __repr__(self):
        return (f"<Header(requestorId={self.requestorId!r}, "
                f"methodName={self.methodName!r}, "
                f"txid={self.txid!r}>")


class Body:
    def __init__(self, documents: list[Document]):
        self.documents = documents

    def __repr__(self):
        return f"<Body(documents={self.documents!r}>"


class Ccd:
    def __init__(self, header: Header, body: Body):
        self.header = header
        self.body = body

    def __repr__(self):
        return f"<Request(header={self.header!r}, body={self.body!r}>"
