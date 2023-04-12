import socket

CLIENT_IP = "127.0.0.1"
CLIENT_PORT = 8820

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((CLIENT_IP, CLIENT_PORT))

    data = ""
    while data != "BYE!!!":
        msg = input("Please enter your msg: ")
        client_socket.send(msg.encode())
        data = client_socket.recv(1024).decode()

        print("The server sent: " + data)