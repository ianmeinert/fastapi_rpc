import json
import socket

from marshmallow import ValidationError

from core.config import settings
from base.base_processor import Processor

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((settings.HOST, settings.PORT))
tcp_socket.listen(settings.THREADS)

print("Waiting for connection")

while True:
    connection, client = tcp_socket.accept()
    print(f"Connected to client IP: {client}")

    while True:
        data = connection.recv(settings.BYTES_SIZE)

        if not data:
            break

        json_obj = json.loads(data.decode("utf-8"))
        print(f"Received data: {json_obj}")

        processor = Processor(json_obj)

        try:
            # validate the message header
            processor.validate_header()
            loaded = processor.load_schema()

            # forwarded to MuleSoft for Adapter processing
            processor.forward_request(loaded, settings.DROPZONE)

            # Validation is complete. Send a response
            response = processor.get_response(msgstatus="OK")
            connection.sendall(response.encode())
        except (ValidationError, KeyError) as err:
            response = processor.get_error_response(err)
            connection.sendall(response.encode())
