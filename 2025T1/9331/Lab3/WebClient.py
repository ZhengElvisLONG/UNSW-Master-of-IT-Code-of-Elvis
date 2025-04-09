import socket
import os

def start_server(host='127.0.0.1', port=49152):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is up and running at {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Got a connection from {client_address}")
        handle_request(client_socket)

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print(f"Request received:\n{request}")

    request_line = request.splitlines()[0]
    print(f"Request line: {request_line}")

    if request_line.startswith('GET'):
        file_path = request_line.split()[1]
        if file_path == '/':
            file_path = '/index.html'

        try:
            with open('.' + file_path, 'rb') as file:
                file_content = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += f"Content-Length: {len(file_content)}\r\n"
            response += f"Content-Length: {len(file_content)}\r\n"
            response += "Connection: keep-alive\r\n"
            response += "\r\n"
            response = response.encode() + file_content
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += "Connection: keep-alive\r\n"
            response += "\r\n"
            response += "<h1>404 Not Found</h1>"
            response = response.encode()
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += "Connection: keep-alive\r\n"
        response += "\r\n"
        response += "<h1>404 Not Found</h1>"
        response = response.encode()

    client_socket.sendall(response)
    client_socket.close()

if __name__ == '__main__':
    start_server()
