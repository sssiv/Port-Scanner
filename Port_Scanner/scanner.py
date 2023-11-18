import socket 

# Helps speed up scanning speed
import threading

# Used to collect all ports
from queue import Queue

# Default Gateway
target = input("Enter Target: ")

# Desired Port range
port_range = input("Enter Port Range: ")

# Split the port range into 2 inputs
first, last = map(int, port_range.split())

# List of which port numbers to scan
ports_list = range(first, last + 1)
# Queue of ports
queue = Queue()

# List of open ports
open_ports = []

# Scans individual port
def portscan(port):
    # Try making a connection
    try:
        # Make a socket to connect to target
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Except, if a connection times out, it is likely unable to connect
        scanner.settimeout(1)

        # Connect to target default gateway. If target + port connect, then the port is open
        scanner.connect((target, port))

        # Connection Succeded
        return True
    
    # Connection Failed
    except:
        return False

# Makes Queue of ports
def collect_ports(ports):
    for port in ports:
        queue.put(port)

# What actually scans all ports
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"Port {port} is open")
            open_ports.append(port)


# Collect ports into the queue
collect_ports(ports_list)

# List of each thread 
thread_list = []

# Takes in how many threads to take in. How many ports are scanned simultaniously 
# What port range is scanned at a time
# In this case port 0-250, then 250-500 and so on
for i in range(250):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# Starts each thread
for thread in thread_list:
    thread.start()

# Makes sure that each thread completes
for thread in thread_list:
    thread.join()

# Display Open ports
print("Open ports are ", open_ports)