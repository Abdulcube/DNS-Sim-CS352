# Abdulrahman Abdulrahman (aa1684) and Manav Patel (mjp430)
import socket
import sys

# Opens file and gets all ip addresses needed
# Stores it in db dictionary
def read_dnsrs():
    file = open('PROJI-DNSRS.txt', 'r')
    database = file.readlines()
    db= {}

    for line in database:
        list = line.strip('\n').split(" ")
        if list[2] == "A":
            db[list[0].lower()] = list[1] + " A"
        if list[2] == "NS":
            db["NS"] = list[0]+ " NS"

    #print(db)
    return db

def rserver():
    # Make sure we have a port number
    if len(sys.argv) != 2:
        print("Error: Please use the proper command: python rs.py rsListenPort")
        exit()

    # Sets the ports and hosts
    PORT = int(sys.argv[1])

    # Get DNS file
    db = read_dnsrs()

    try:
        connectSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[S]: Server socket created")
    except socket.error as err:

        print("Socket Opening error")
        exit()
    #host address :
    connectSock.bind(("0.0.0.0", PORT))

    connectSock.listen(1)

    while True:
        conn, addr = connectSock.accept()
        print("Connection to address: ", addr)

        #with conn:
        data = conn.recv(1024).decode("utf-8")
        print(data)

        # Checks in our dictionary, if not sends the localhost
        if data in db:
            conn.sendall(str.encode(db[data]))
        else:
            conn.sendall(str.encode(db["NS"]))


if __name__ == "__main__":
    rserver()
