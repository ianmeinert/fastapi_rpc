import asyncio
import json
import uuid

from marshmallow import ValidationError

from core.config import settings
from base.base_processor import Processor

host = settings.HOST
port = settings.PORT
read_len = settings.BYTES_SIZE

tasks = []


async def get_response(data):
    json_obj = json.loads(data)
    print(f"Received data: {json_obj}")

    txid = uuid.uuid4().hex
    processor = Processor(txid, json_obj)

    try:
        # validate the message header
        processor.validate_header()
        loaded = processor.load_schema()

        # forwarded to MuleSoft for Adapter processing
        processor.forward_request(loaded, settings.DROPZONE)

        # Validation is complete. Send a response
        response = processor.get_response(msgstatus="OK")
        return response
    except (ValidationError, KeyError) as err:
        response = processor.get_error_response(err)
        return response


async def handle_client(reader, writer):
    request = None
    request = (await reader.read(read_len))
    response = await get_response(request.decode("utf-8"))
    writer.write(response.encode('utf8'))
    await writer.drain()
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_client, host, port)
    print("Waiting for connection")
    async with server:
        await server.serve_forever()


asyncio.run(run_server())
