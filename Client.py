import socket
import time
import sys
 
TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
MESSAGE = sys.argv[3]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
send_time_ms=time.time()
s.send(MESSAGE.encode('utf-8'))
data = s.recv(BUFFER_SIZE)
recv_time_ms=time.time()
rtt=round(recv_time_ms-send_time_ms,3)

def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

print ("Family  :", families[s.family])
print ("Type    :", types[s.type])
print ("Protocol:", protocols[s.proto])
 
print ("received data:", data)
print("Round Trip Time :   ",rtt)
print("Hostname    : ",socket.gethostname())
#print("Peername : ",socket.getpeername())
s.close()

