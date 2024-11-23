import requests
import socket
import threading

def handle_client(client_socket):
    """Handles the communication with the client."""
    while True:

        data = client_socket.recv(1024)
        if not data:
            print("Connection closed by client.")
            break
        print(f"Received from client: {data.decode()}") 
        client_socket.sendall(data) 




    client_socket.close()

def server():
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

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

    while True:
        command = input("Enter a command to send to the client (or type 'exit' to close): ")
        if command.lower() == 'exit':
            print("Closing connection.")
            client_socket.close()
            break
        client_socket.sendall(command.encode())

        response = client_socket.recv(1024)
        if not response:
            print("No response from client.")
            break
        print(f"Client response: {response.decode()}")
    s.close()

if __name__ == "__main__":
    server()
