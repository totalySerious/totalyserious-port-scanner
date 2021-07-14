import socket
import threading
from queue import Queue
import time

target = '127.0.0.1'
queue = Queue()
open_ports = []

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f'port {port} open!')
            open_ports.append(port)

port_list = range(0, 1024*4)
fill_queue(port_list)

thread_list = []

star_time = time.time()

for t in range(500):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thd in thread_list:
    thd.start()

for thread in thread_list:
    thread.join()

end_time = time.time()

print(int(end_time - star_time), 'seconds')

print('ports open: ', open_ports)
