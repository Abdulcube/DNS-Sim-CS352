import socket

file = open('PROJI-HNS.txt', 'r')
queries = file.readlines()

for line in queries:
    query = line.strip('\n').lower()
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(query))
        data = s.recv(1024)
        print(query + " :: " + data.decode("utf-8") )
