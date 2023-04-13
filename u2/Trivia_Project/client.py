import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(connect_socket, cmd: str, data: str):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    format_msg = chatlib.build_message(cmd, data)
    connect_socket.send(format_msg.encode())


def recv_message_and_parse(connect_socket):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # Implement Code
    # ..
    full_msg = connect_socket.recv(1024)
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_socket.connect((SERVER_IP, SERVER_PORT))
    return connect_socket


def error_and_exit(error_msg: str):
    print(error_msg)
    exit()


def login(connect_socket):
    check = chatlib.PROTOCOL_SERVER["login_failed_msg"]
    while check == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
        username = input("Please enter username: ")
        password = input("Please enter password: ")
        build_and_send_message(connect_socket, chatlib.PROTOCOL_CLIENT["login_msg"], username + "#" + password)
        cmd, data = recv_message_and_parse(connect_socket)
        if cmd is not None:
            check = chatlib.PROTOCOL_SERVER["login_ok_msg"]
            print(check)


def logout(connect_socket):
    build_and_send_message(connect_socket, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def main():
    connect_socket = connect()
    login(connect_socket)
    logout(connect_socket)
    connect_socket.close()


if __name__ == '__main__':
    main()
