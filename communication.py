import requests
import socket
import threading

user_connections = []



def mainmenu():
    print(f"{user_connections[0]}: 1")
    connectionbranch = input("enter the connection you want")
    if connectionbranch == 1 or "1":
        print(f"trying to connect to {user_connections[0]}")
        communication(user_connections[0])

def handle_client(client_socket):
    while True:

        data = client_socket.recv(1024)
        if not data:
            print("Connection closed by client.")
            break
        print(f"Received from client: {data.decode()}") 
        client_socket.sendall(data) 

    client_socket.close()

def server():
    global s
    global client_socket
    link = "https://raw.githubusercontent.com/80dropz/communication/refs/heads/main/ipv4.txt"
    data = requests.get(link)
    hostip = data.text.strip() 
    port = 65432
    print(f"Server will listen on {hostip}:{port}")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostip, port))
    print(f"Binding to {hostip} on port {port}")

    s.listen(5)

    client_socket, addr = s.accept()
    print(f"Connection received from {addr}")
    userlist = client_socket.recv(1024).decode()
    user = userlist, client_socket
    user_connections.append((user))
    print(user_connections)
    mainmenu()



def communication(socket):
    while True:
        command = input("Enter a command to send to the client (or type 'exit' to close): ")
        if command.lower() == 'exit':
            print("Closing connection.")
            mainmenu()
        client_socket.sendall(command.encode())

        response = client_socket.recv(1024)
        if not response:
            print("No response from client.")
            break
        print(f"Client response: {response.decode()}")
    s.close()

if __name__ == "__main__":
    server()
