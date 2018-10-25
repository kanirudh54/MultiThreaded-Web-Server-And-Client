import socket  # Networking support
import signal  # Signal support (server shutdown on signal receive
import time    # Current time
import sys     # To Take input from command Line 
import webbrowser # Open WebBrowser
import threading  #For Thread
import os
from datetime import datetime 

class Server:

 """ a simple HTTP server objects."""

 def __init__(self, port):
     """ C """
     self.host = '127.0.0.1'   # <-- works on all avaivable network interfaces
     print("port:",port)
     self.port = port
     self.www_dir = os.getcwd() #'C:\\' #Directory for webpage Files are Stored.

 def start_server(self):

     """  the socket and launch the server """

     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     try: # user provided in the __init__() port may be unavaivable
         print("Launching HTTP server on ", self.host, ":",self.port)
         self.socket.bind((self.host, self.port))
     except Exception as e:

         print ("Warning: Could not aquite port:",self.port,"\n")
         print ("Trying a higher port")
         # store to user provideed port locally for later (in case 8080 fails)
         use_port = self.port
         self.port = 8080

         try:
             print("Launching HTTP server on ", self.host, ":",self.port)
             self.socket.bind((self.host, self.port))
         except Exception as e:
             print("ERROR: Failed to acquire sockets for ports ", use_port, " and 8080. ")
             print("Try running the Server in a privileged user mode.")
             self.shutdown()
             sys.exit(1)

     print ("Server successfully acquired the socket with port:", self.port)
     self.waiting_for_connections()

 def shutdown(self):

     """ Shut down """

     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)

 def generate_headers(self,  code, file_modifiedtime):

     """ Generates HTTP response Headers. """

     #  response code
     h = ''
     if (code == 200):      # If The Html file is present response is OK
        h = 'HTTP/1.1 200 OK\n'
        h += 'Last-Modified:' + str(datetime.fromtimestamp(file_modifiedtime).strftime("%a, %d %b %Y %H:%M:%S")) + ' \n'
     elif(code == 404):     #If the Html file is not there response is 404 Not Found 
        h = 'HTTP/1.1 404 Not Found\n'

     #headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request
     return h

 def waiting_for_connections(self):

     """ Main loop awaiting connections """

     while True:
         print ("Awaiting New connection")
         self.socket.listen(100) #Maximum Nummber Of Queued Connections
         conn, addr = self.socket.accept()
         # conn - socket to client
         # addr - clients address
         print("Got connection from:", addr)
         print("Protocol : ", conn.proto)
         print("Type : ", conn.type)
         print("Family Socket", conn.family)
         print("Peername",conn.getpeername())
         print("TimeOut :  ",conn.gettimeout())
         client_handler = threading.Thread(target=self.handle_client, args=(conn,)) # Creating Thread For Client using threading module
         client_handler.start() # starting the thread

 def handle_client(self,client_socket):
     #Thread
    data = client_socket.recv(1024) #  receive Data From Client
    print ("[*] Received: " , data)
    string = bytes.decode(data)  # Decode It to String
    #Determine Request Method Get and Head are Supported)
    request_method=string.split(" ")[0]
    print("Method: ", request_method)
    print("Request Body: ", string)
    if (request_method == 'GET') | (request_method == 'HEAD'):
       file_request = string.split(' ')
       file_request = file_request[1]
       file_request = file_request.split('?')[0]
       if (file_request == '/'):
            file_request = '/index.html'
       file_request = self.www_dir + file_request
       print ("Serving web page [",file_request,"]")
       print ("Remove later", file_request)
        ## Load file content
       try:
           file_handler = open(file_request,'rb')
           file_modifiedtime = os.path.getmtime(file_request)
           print(file_handler, file_modifiedtime)
           if (request_method == 'GET'):
               response_content = file_handler.read()
           file_handler.close()
           response_headers = self.generate_headers(200, file_modifiedtime)
           if (request_method == 'GET'):
               webbrowser.open(file_request) #Open The Html File On browser only if it is a GET request
       except Exception as e: # not found, generate 404 page
           print ("Warning, file not found. Serving response code 404\n",e)
           response_headers = self.generate_headers( 404, file_modifiedtime)
           if (request_method == 'GET'):
                  response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
                  webbrowser.open(os.getcwd() + "/404.html")  #Open The HTML File on The Browser 
       server_response =  response_headers.encode() #return Header for Get and Head
       if (request_method == 'GET'):
           server_response +=  response_content # return Additional Content
       client_socket.send(server_response)
       print ("Closing connection with client")
       client_socket.close()
       print ("Awaiting New connection")
    else:
        print("Unknown HTTP request method:", request_method)
        print ("Awaiting New connection")


p= int(sys.argv[1])
print("p:",p)
print ("Starting web server")

s = Server(p)  # construct server object

s.start_server() # aquire the socket
