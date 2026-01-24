import socket
import database

# database initialization
database.init_database()

# create-server-socker

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# AF_INET - Internet Protocol v4 addresses
# SOCK_STREAM - TCP protocol

host = "127.0.0.1"
port = 8080

# bind-server-socket

server_socket.bind((host, port))
# makes the server-listen-to-the-specified-port


# setup-listening

server_socket.listen(3)
# puts-the-server-in-listening-mode

# accept-connections

client_socket, addr = server_socket.accept()
print("Connection from :", str(addr) + "has been established!")

# Authentication
authenticated = False  # flag to check if user is authenticated
username = None  # empty variable to hold username later

try:
    client_socket.sendall("Authentication Required \n 1. Register \n 2. Login".encode())
    action = (
        client_socket.recv(1024).decode().strip()
    )  # receive action choice for registration or login

    if action == "1":  # Registration process
        client_socket.sendall("Enter Username".encode())
        username = client_socket.recv(1024).decode().strip()

        client_socket.sendall("Enter Password".encode())
        password = client_socket.recv(1024).decode().strip()

        success, message = database.register_user(
            username, password
        )  # register user in database

        if success:
            client_socket.sendall(f"SUCCESS:{message}".encode())
            print(f"User '{username}' registered successfully!")
            authenticated = True
        else:
            client_socket.sendall(f"FAILURE:{message}".encode())
            print(f"Registration failed: {message}")
            client_socket.close()
            server_socket.close()
            exit()
    elif action == "2":  # Login process
        client_socket.sendall("Enter Username".encode())
        username = client_socket.recv(1024).decode().strip()

        client_socket.sendall("Enter Password".encode())
        password = client_socket.recv(1024).decode().strip()

        success, message = database.verify_user(
            username, password
        )  # authenticate user in database

        if success:
            client_socket.sendall(f"SUCCESS:{message}".encode())
            print(f"User '{username}' logged in successfully!")
            authenticated = True
        else:
            client_socket.sendall(f"FAILURE:{message}".encode())
            print(f"Authentication failed: {message}")
            client_socket.close()
            server_socket.close()
            exit()
    else:  # Invalid action like anything other than 1 or 2
        client_socket.sendall("Invalid action. Connection closing.".encode())

except Exception as e:
    print(f"Error during authentication: {e}")
    client_socket.close()
    server_socket.close()
    exit()
if not authenticated:  # check if user is not authenticated
    print("Authentication failed. Closing connection.")
    client_socket.close()
    server_socket.close()
    exit()

print(f"User '{username}' connected. Type 'stop' to end the connection")

while True:
    # receive-message-from-client
    data = client_socket.recv(1024).decode()
    if not data:
        print("Client disconnected")
        break
    print(f"Client: {data}")

    # check-for-stop-condition(received-from-client)

    if data.strip().lower() == "stop":
        print("stop command received. closing the connection now.")
        break

    # send-response-to-client

    server_data = input("Server:")
    client_socket.sendall(server_data.encode())

    # check-for-stop-command(sent-from-server)

    if server_data.strip().lower() == "stop":
        print("stop command sent. closing the connection now.")
        break

# close-sockets

client_socket.close()
server_socket.close()
print("Server closed.")
