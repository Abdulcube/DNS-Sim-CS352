import socket
import sys
#Opens file and gets all ip addresses needed
#Stores it in db dictionary
file = open('PROJI-DNSRS.txt', 'r')
database = file.readlines()
db= {}
for line in database:
    list = line.strip('\n').split(" ")
    if list[2] == "A":
        db[list[0].lower()] = list[1] + " A"
    if list[2] == "NS":
        db["NS"] = list[0]+ " NS"

print(db)
#Sets the ports and hosts
HOST = "127.0.0.1"
PORT = int(sys.argv[1])

#Loops and listens to connections
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("\n")
        pass
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print("Connected to ", addr )

        with conn:
            data = conn.recv(1024).decode("utf-8")
            print(data)
            #Checks in our dictionary, if not sends the localhost
            if data in db:
                conn.sendall(str.encode(db[data]))
            else:
                conn.sendall(str.encode(db["NS"]))
