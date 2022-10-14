import socket

HOST = "localhost"  # The remote host
PORT = 50007  # The same port as used by the server
bytes_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    path = "data/init_req.json"

    with open(path, "r") as f:
        tx_data = f.read()
        print("Sending", tx_data)
        byte_size = len(tx_data)

        tcp_socket.connect((HOST, PORT))
        tcp_socket.sendall(tx_data.encode())

    data = tcp_socket.recv(byte_size)
print("Received", data.decode())
