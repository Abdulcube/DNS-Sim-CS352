import socket
import os
import sys

def client():
    # Check if we have the proper arguments
    if len(sys.argv) != 4:
        print("Error: Please use the proper command: python client.py rsHostname rsListPort tsListenPort")
        exit()
    
    # Read the list of domains
    file = open('PROJI-HNS.txt', 'r')
    queries = file.readlines()

    # If RESOLVED.txt previously existed, remove it so we can create and append to a new file
    try:
        os.remove("RESOLVED.txt")
    except OSError:
        pass
    resolved = open("RESOLVED.txt", "a")

    # Loop through each domain name and connect to our rs and/or ts for DNS lookups
    for line in queries:
        query = line.strip('\n').lower()
        """HOST = '127.0.0.1'
        TPORT = 26577
        PORT = 26844"""

        HOST = sys.argv[1]
        # Make sure our ports are integers
        try:
            PORT = int(sys.argv[2])
            TPORT = int(sys.argv[3])
        except ValueError:
            print("Error: Please ensure you are using proper Ports")
            exit()

        # Connect to the RS
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            AHOST = socket.gethostbyname(HOST)
            #print("[C]: Client socket created")
        except socket.error as err:
            print('socket open error: {} \n'.format(err))
            exit()

        # Send the host name for DNS lookup
        cs.connect((AHOST, PORT))
        cs.sendall(str.encode(query))

        # Receive lookup from RS
        data = cs.recv(1024)
        code = data.decode("utf-8").split(" ")

        # If found in RS, write to RESOLVED.txt, else continue lookup in TS
        if code[1] == "A" :
            resolved.write(query + " " + code[0] + " A\n")
            print(query + " - " + code[0] + " A")
        else:
            # Connect to the TS
            try:
                ct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #print("[C]: Client socket created")
            except socket.error as err:
                print('socket open error: {} \n'.format(err))
                exit()

            # Send the host name for DNS lookup
            ct.connect((code[0], TPORT))
            ct.sendall(str.encode(query))

            # Receive lookup from TS
            data = ct.recv(1024)
            code = data.decode("utf-8")

            # If query returned "NS", write Host Not Found to file, otherwise write the reponse to file
            if code == "NS" :
                resolved.write(query + " - " + "Error:HOST NOT FOUND\n")
                print(query + " - " + "Error:HOST NOT FOUND")
            else:
                resolved.write(query + " " + code + " A\n")
                print(query + " " + code + " A")
    print("Done")


if __name__ == "__main__":
    client()
