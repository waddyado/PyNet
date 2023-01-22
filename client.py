import socket, time, os

#toggle dev mode
verbose = True


addr = ('127.0.0.1', 5002)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init():
        while True:
                try:
                        client.connect(addr)
                        client.send('client'.encode('utf-8'))
                        break
                except:
                        print(f'[NOTICE] Could not connect to {addr[0]}:{addr[1]}')
        main()

def main():
        if verbose:
                print(f'[CONNECTED] Connected to {addr[0]}:{addr[1]}')
        while True:
                msg = client.recv(1024)
                if msg:
                    print('command recieved:', msg.decode('utf-8'))
                    time.sleep(1)
                    client.send(msg)
                    '''
                    Shell Code
                    time.sleep(1)
                    output_stream = os.popen(msg.decode('utf-8'))
                    output = output_stream.read()
                    client.send(output.encode('utf-8'))
                    '''
            



init()
