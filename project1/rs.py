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
    # Sets the ports and hosts
    HOST = "0.0.0.0"
    PORT = int(sys.argv[1])

    # Get DNS file
    db = read_dnsrs()

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    ss.bind((HOST, PORT))
    ss.listen(1)

    while True:
        conn, addr = ss.accept()
        print("Connected to ", addr)

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