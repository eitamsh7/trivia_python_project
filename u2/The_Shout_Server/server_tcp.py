import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8820

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Server is up and running...")

    (client_socket, client_address) = server_socket.accept()
    print("Client Connected")

    while True:
        data = client_socket.recv(1024).decode()
        print("The client sent: " + data)
        if data == "quit":
            print("Closing client socket now...")
            client_socket.send("BYE!!!".encode())
            break
        client_socket.send(f"{data.upper()}!!!".encode())
    client_socket.close()