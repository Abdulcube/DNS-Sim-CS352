import socket

file = open('PROJI-HNS.txt', 'r')
queries = file.readlines()

for line in queries:
    query = line.strip('\n').lower()
    HOST = '127.0.0.1'
    TPORT = 26578
    PORT = 65432

    """HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    TPORT = int(sys.argv[3])"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(str.encode(query))
        data = s.recv(1024)
        code = data.decode("utf-8").split(" ")
        if code[1] == "A" :
            print(query + " :: " + code[0] )
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as t:
                t.connect((code[0], TPORT))
                t.sendall(str.encode(query))
                data = t.recv(1024)
                code = data.decode("utf-8")
                if code == "L" :
                    print(query + " - " + "Error:HOST NOT FOUND" )
                else:
                    print(query + " :: " + code )
