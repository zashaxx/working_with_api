import socket

# create-client-socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8080

# connect-to-server
client_socket.connect((host, port))
# Authentication process
try:
    auth_message = client_socket.recv(
        1024
    ).decode()  # relays authentication message from server
    print(auth_message)

    choice = input(
        "Enter your choice :"
    ).strip()  # get user choice for registration or login
    client_socket.sendall(choice.encode())  # send choice to server
    prompt = client_socket.recv(1024).decode()  # receive prompt from server
    if prompt == "Enter Username":
        username = input("Enter Username: ").strip()
        client_socket.sendall(username.encode())  # send username to server

        prompt = client_socket.recv(1024).decode()
        if prompt == "Enter Password":
            password = input("Enter Password: ").strip()
            client_socket.sendall(password.encode())  # send password to server

            response = client_socket.recv(1024).decode()  # receive response from server
            if response.startswith("SUCCESS:"):
                message = response.split(":", 1)[1]
                print(f"Authentication successful: {message}")
            elif response.startswith("FAILURE:"):
                message = response.split(":", 1)[1]
                print(f"Authentication failed: {message}")
                client_socket.close()
                exit()
            else:
                print(f"Invalid response format: {response}")
                client_socket.close()
                exit()
except Exception as e:
    print(f"Error during authentication: {e}")
    client_socket.close()
    exit()

print(
    f"user {username} authenticated successfully. You are now connected. Type 'stop' to end the connection."
)


while True:
    # send-message-to-server

    message = input("Client:")
    client_socket.sendall(message.encode())

    # check-for-stop-command(sent-from-client)

    if message.strip().lower() == "stop":
        print("stop command sent. closing the connection now.")
        break

    # receive-response-from-server

    data = client_socket.recv(1024).decode()
    if not data:
        print("Server disconnected")
        break
    print(f"Server: {data}")

    # check-for-stop-condition(received-from-server)

    if data.strip().lower() == "stop":
        print("stop command received. closing the connection now.")
        break
